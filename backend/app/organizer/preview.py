from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from sqlalchemy import select

from app.config import settings
from app.database import SessionLocal
from app.models.photo import Photo


def _preserve_filename(name: str) -> str:
    """
    Preserve the original filename, including spaces and Unicode characters.
    Only path separators and NUL are replaced because they cannot safely be
    part of a single destination filename.
    """
    cleaned = name.replace("/", "_").replace("\\", "_").replace("\x00", "_").strip()
    return cleaned or "media"


def _normal_destination(photo: Photo) -> Path:
    filename = _preserve_filename(photo.filename)
    if photo.captured_at:
        folder = (
            settings.organizer_root
            / photo.captured_at.strftime("%Y")
            / photo.captured_at.strftime("%m")
        )
        return folder / filename
    return settings.unknown_date_root / filename


def _duplicate_destination(photo: Photo) -> Path:
    filename = _preserve_filename(photo.filename)
    if photo.captured_at:
        folder = (
            settings.duplicate_root
            / photo.captured_at.strftime("%Y")
            / photo.captured_at.strftime("%m")
        )
    else:
        folder = settings.duplicate_root / "UnknownDate"
    return folder / filename


def _make_unique(path: Path, used: set[str]) -> Path:
    candidate = path
    index = 2
    while str(candidate).casefold() in used:
        candidate = candidate.with_name(f"{path.stem}__{index}{path.suffix}")
        index += 1
    used.add(str(candidate).casefold())
    return candidate


def build_preview(root_path: str | None = None, limit: int | None = None, exclude_paths: list[str] | None = None) -> dict:
    with SessionLocal() as session:
        stmt = select(Photo).order_by(Photo.path)
        if root_path:
            normalized = root_path.rstrip("/")
            stmt = stmt.where(Photo.path.like(normalized + "/%"))

        # Duplicate detection must use the COMPLETE filtered collection.
        # The display limit is applied only after the plan is built.
        photos = list(session.scalars(stmt).all())

        normalized_excludes = [x.rstrip("/") for x in (exclude_paths or []) if x.strip()]
        if normalized_excludes:
            photos = [
                photo for photo in photos
                if not any(
                    photo.path == excluded or photo.path.startswith(excluded + "/")
                    for excluded in normalized_excludes
                )
            ]

        hash_groups: dict[str, list[Photo]] = defaultdict(list)
        for photo in photos:
            if photo.checksum_sha256:
                hash_groups[photo.checksum_sha256].append(photo)

        duplicate_ids: set[int] = set()
        keep_ids: set[int] = set()

        for items in hash_groups.values():
            if len(items) > 1:
                ordered = sorted(items, key=lambda p: p.path.casefold())
                keep_ids.add(ordered[0].id)
                duplicate_ids.update(item.id for item in ordered[1:])

        used_destinations: set[str] = set()
        all_actions = []
        counts = {
            "organize": 0,
            "duplicate": 0,
            "unknown_date": 0,
            "name_collisions_resolved": 0,
        }

        for photo in photos:
            if photo.id in duplicate_ids:
                proposed = _duplicate_destination(photo)
                action = "duplicate"
                reason = (
                    "Exact SHA-256 duplicate; preview routes this extra copy "
                    "to the duplicate tree."
                )
            else:
                proposed = _normal_destination(photo)
                action = "organize"
                reason = (
                    "Primary/unique media; preview organizes by capture year "
                    "and month while preserving the original filename."
                )
                if photo.captured_at is None:
                    action = "unknown_date"
                    reason = (
                        "No capture date available; preview routes this item "
                        "to UnknownDate while preserving the original filename."
                    )

            before = proposed
            proposed = _make_unique(proposed, used_destinations)
            collision_resolved = proposed != before
            if collision_resolved:
                counts["name_collisions_resolved"] += 1

            counts[action] += 1
            all_actions.append({
                "media_id": photo.id,
                "action": action,
                "source": photo.path,
                "original_filename": photo.filename,
                "proposed_destination": str(proposed),
                "captured_at": photo.captured_at,
                "checksum_sha256": photo.checksum_sha256,
                "exact_duplicate": photo.id in duplicate_ids,
                "primary_duplicate_copy": photo.id in keep_ids,
                "collision_resolved": collision_resolved,
                "reason": reason,
            })

        actions = all_actions if limit is None else all_actions[:limit]

        return {
            "mode": "dry-run",
            "writes_enabled": False,
            "root_filter": root_path,
            "excluded_paths": normalized_excludes,
            "total_media_in_plan": len(all_actions),
            "returned_actions": len(actions),
            "limit": limit,
            "summary": counts,
            "actions": actions,
        }
