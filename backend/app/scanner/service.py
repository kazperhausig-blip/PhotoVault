from datetime import datetime
from pathlib import Path
from typing import Iterator
import os

from loguru import logger
from sqlalchemy import select

from app.config import settings
from app.database import SessionLocal
from app.metadata.extractor import extract_metadata
from app.models.photo import Photo
from app.models.scan_job import ScanJob
from app.scanner.extensions import SUPPORTED_EXTENSIONS, media_type_for_extension
from app.scanner.hashing import sha256_file
from app.scanner import state


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def validate_scan_root(requested: Path | None) -> Path:
    root = (requested or settings.scan_root).resolve()
    storage = settings.storage_path.resolve()

    if not root.exists():
        raise ValueError(f"Scan path does not exist: {root}")
    if not root.is_dir():
        raise ValueError(f"Scan path is not a directory: {root}")
    if not _is_within(root, storage):
        raise ValueError("Scan path must be inside the configured storage tree")
    return root



def _normalize_exclusions(requested: list[Path] | None = None) -> list[Path]:
    """Return global + request exclusions, safely constrained to /storage."""
    storage = settings.storage_path.resolve()
    exclusions = [p.resolve() for p in settings.excluded_paths]

    for item in requested or []:
        resolved = item.resolve()
        if not _is_within(resolved, storage):
            raise ValueError(f"Excluded path must be inside the configured storage tree: {item}")
        exclusions.append(resolved)

    return exclusions


def _is_excluded(path: Path, exclusions: list[Path]) -> bool:
    resolved = path.resolve()
    return any(_is_within(resolved, excluded) for excluded in exclusions)


def discover_media(root: Path, requested_exclusions: list[Path] | None = None) -> Iterator[Path]:
    exclusions = _normalize_exclusions(requested_exclusions)

    for current_root, dirnames, filenames in os.walk(root):
        current = Path(current_root)
        dirnames[:] = [
            name for name in dirnames
            if not _is_excluded(current / name, exclusions)
            and not name.startswith(".")
            and name not in {"@eaDir", "#recycle", ".Trash", ".Trashes"}
        ]

        for filename in filenames:
            if filename.startswith("."):
                continue
            path = current / filename
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                yield path
def create_scan_job(root: Path) -> int:
    with SessionLocal() as session:
        job = ScanJob(status="queued", root_path=str(root), started_at=datetime.utcnow())
        session.add(job)
        session.commit()
        session.refresh(job)
        return job.id


def run_scan(job_id: int, root: Path, requested_exclusions: list[Path] | None = None) -> None:
    if not state.begin(job_id=job_id, root_path=str(root)):
        logger.warning("A scan is already running")
        return

    with SessionLocal() as session:
        job = session.get(ScanJob, job_id)
        if job is None:
            state.finish()
            return

        job.status = "running"
        session.commit()

        try:
            for path in discover_media(root, requested_exclusions):
                state.increment("discovered")
                state.update(current_file=str(path))
                job.discovered = state.snapshot()["discovered"]

                try:
                    stat = path.stat()
                    modified_at = datetime.fromtimestamp(stat.st_mtime)
                    now = datetime.utcnow()
                    existing = session.scalar(select(Photo).where(Photo.path == str(path)))
                    media_type = media_type_for_extension(path.suffix)

                    unchanged = (
                        existing is not None
                        and existing.size_bytes == stat.st_size
                        and existing.modified_at == modified_at
                        and existing.checksum_sha256
                        and existing.metadata_status is not None
                    )

                    if unchanged:
                        existing.last_seen_at = now
                        state.increment("skipped_unchanged")
                        job.skipped_unchanged = state.snapshot()["skipped_unchanged"]
                        session.commit()
                        continue

                    checksum = sha256_file(path)
                    metadata = extract_metadata(path, media_type)

                    if existing is None:
                        existing = Photo(
                            path=str(path),
                            filename=path.name,
                            extension=path.suffix.lower(),
                            size_bytes=stat.st_size,
                            checksum_sha256=checksum,
                            modified_at=modified_at,
                            media_type=media_type,
                            last_seen_at=now,
                        )
                        session.add(existing)
                    else:
                        existing.filename = path.name
                        existing.extension = path.suffix.lower()
                        existing.size_bytes = stat.st_size
                        existing.checksum_sha256 = checksum
                        existing.modified_at = modified_at
                        existing.media_type = media_type
                        existing.last_seen_at = now

                    for key, value in metadata.items():
                        setattr(existing, key, value)

                    session.commit()
                    state.increment("indexed")
                    job.indexed = state.snapshot()["indexed"]

                except Exception as exc:
                    session.rollback()
                    state.increment("errors")
                    job.errors = state.snapshot()["errors"]
                    logger.warning("Could not index {}: {}", path, exc)

            snapshot = state.snapshot()
            job.status = "completed"
            job.finished_at = datetime.utcnow()
            job.discovered = snapshot["discovered"]
            job.indexed = snapshot["indexed"]
            job.skipped_unchanged = snapshot["skipped_unchanged"]
            job.errors = snapshot["errors"]
            session.commit()

        except Exception as exc:
            session.rollback()
            job = session.get(ScanJob, job_id)
            if job:
                job.status = "failed"
                job.finished_at = datetime.utcnow()
                job.error_message = str(exc)
                job.errors = state.snapshot()["errors"] + 1
                session.commit()
            logger.exception("Scan failed: {}", exc)
        finally:
            state.finish()
