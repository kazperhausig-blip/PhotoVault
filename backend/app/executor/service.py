from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil

from loguru import logger
from sqlalchemy import select

from app.config import settings
from app.database import SessionLocal
from app.executor import state
from app.models.copy_job import CopyItem, CopyJob
from app.organizer.preview import build_preview
from app.scanner.hashing import sha256_file


def _logical_to_output(logical: str) -> Path:
    # Preview paths are /Photos/... or /Duplicates/...
    relative = logical.lstrip("/")
    destination = (settings.output_path / relative).resolve()
    output_root = settings.output_path.resolve()
    try:
        destination.relative_to(output_root)
    except ValueError as exc:
        raise ValueError("Destination escaped the configured output root") from exc
    return destination


def create_job(source_root: str, exclude_paths: list[str] | None = None) -> int:
    plan = build_preview(root_path=source_root, limit=None, exclude_paths=exclude_paths)
    now = datetime.utcnow()

    with SessionLocal() as session:
        job = CopyJob(
            status="queued",
            source_root=source_root,
            started_at=now,
            total=plan["total_media_in_plan"],
        )
        session.add(job)
        session.flush()

        for action in plan["actions"]:
            if not action["checksum_sha256"]:
                raise ValueError(f"Media {action['media_id']} has no SHA-256 and cannot be copied safely.")
            session.add(CopyItem(
                job_id=job.id,
                media_id=action["media_id"],
                source=action["source"],
                destination=str(_logical_to_output(action["proposed_destination"])),
                expected_sha256=action["checksum_sha256"],
                status="pending",
                attempts=0,
                updated_at=now,
            ))

        session.commit()
        session.refresh(job)
        return job.id


def _copy_one(item: CopyItem) -> tuple[str, str | None]:
    source = Path(item.source)
    destination = Path(item.destination)

    if not source.is_file():
        raise FileNotFoundError(f"Source file not found: {source}")

    # Resume/idempotence: if destination already exists and verifies, keep it.
    if destination.exists():
        if not destination.is_file():
            raise RuntimeError(f"Destination exists but is not a file: {destination}")
        existing_hash = sha256_file(destination)
        if existing_hash == item.expected_sha256:
            return "skipped_verified", existing_hash
        # Never overwrite an unexpected file.
        raise FileExistsError(
            f"Destination already exists with a different SHA-256: {destination}"
        )

    destination.parent.mkdir(parents=True, exist_ok=True)

    # Copy to a temporary sibling first, then verify, then atomically rename.
    temp = destination.with_name(destination.name + ".photovault-part")
    if temp.exists():
        temp.unlink()

    try:
        shutil.copy2(source, temp)
        copied_hash = sha256_file(temp)
        if copied_hash != item.expected_sha256:
            raise IOError(
                f"Hash verification failed for {source}: "
                f"expected {item.expected_sha256}, got {copied_hash}"
            )
        temp.replace(destination)
        return "verified", copied_hash
    except Exception:
        if temp.exists():
            temp.unlink()
        raise


def run_job(job_id: int) -> None:
    with SessionLocal() as session:
        job = session.get(CopyJob, job_id)
        if job is None:
            return
        items = list(session.scalars(
            select(CopyItem).where(CopyItem.job_id == job_id).order_by(CopyItem.id)
        ).all())

    if not state.begin(job_id, len(items)):
        return

    with SessionLocal() as session:
        job = session.get(CopyJob, job_id)
        job.status = "running"
        session.commit()

        try:
            for item in session.scalars(
                select(CopyItem).where(CopyItem.job_id == job_id).order_by(CopyItem.id)
            ).all():
                state.update(current_source=item.source)
                job.current_source = item.source

                if item.status in {"verified", "skipped_verified"}:
                    state.increment("skipped_verified")
                    job.skipped_verified += 1
                    session.commit()
                    continue

                item.attempts += 1
                item.updated_at = datetime.utcnow()
                item.status = "copying"
                session.commit()

                try:
                    result, digest = _copy_one(item)
                    item.destination_sha256 = digest
                    item.status = result
                    item.error_message = None
                    item.updated_at = datetime.utcnow()

                    if result == "verified":
                        state.increment("copied")
                        state.increment("verified")
                        job.copied += 1
                        job.verified += 1
                    else:
                        state.increment("skipped_verified")
                        job.skipped_verified += 1

                except Exception as exc:
                    item.status = "failed"
                    item.error_message = str(exc)
                    item.updated_at = datetime.utcnow()
                    state.increment("failed")
                    job.failed += 1
                    logger.warning("Copy failed for {}: {}", item.source, exc)

                session.commit()

            job.finished_at = datetime.utcnow()
            job.current_source = None
            job.status = "completed" if job.failed == 0 else "completed_with_errors"
            session.commit()

        except Exception as exc:
            session.rollback()
            job = session.get(CopyJob, job_id)
            if job:
                job.status = "failed"
                job.finished_at = datetime.utcnow()
                job.error_message = str(exc)
                session.commit()
            logger.exception("Copy job failed: {}", exc)
        finally:
            state.finish()
