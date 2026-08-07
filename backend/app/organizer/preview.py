from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import re

from sqlalchemy import select

from app.config import settings
from app.database import SessionLocal
from app.models.photo import Photo


_SAFE_CHARS = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_filename(name: str) -> str:
    cleaned = _SAFE_CHARS.sub("_", name.strip())
    cleaned = cleaned.strip("._")
    return cleaned or "media"


def _date_prefix(captured_at: datetime | None) -> str | None:
    if captured_at is None:
        return None
    return captured_at.strftime("%Y-%m-%d_%H-%M-%S")


def _normal_destination(photo: Photo) -> Path:
    filename = _safe_filename(photo.filename)
    if photo.captured_at:
        folder = settings.organizer_root / photo.captured_at.strftime("%Y") / photo.captured_at.strftime("%m")
        prefix = _date_prefix(photo.captured_at)
        return folder / f"{prefix}_{filename}"
    return settings.unknown_date_root / filename


def _duplicate_destination(photo: Photo) -> Path:
    filename = _safe_filename(photo.filename)
    if photo.captured_at:
        folder = settings.duplicate_root / photo.captured_at.strftime("%Y") / photo.captured_at.strftime("%m")
    else:
        folder = settings.duplicate_root / "UnknownDate"
    return folder / filename


def _make_unique(path: Path, used: set[str]) -> Path:
    candidate = path
    index = 2
    while str(candidate).lower() in used:
        candidate = candidate.with_name(f"{path.stem}__{index}{path.suffix}")
        index += 1
    used.add(str(candidate).lower())
    return candidate


def build_preview(root_path: str | None = None, limit: int | None = None) -> dict:
    with SessionLocal() as session:
        stmt = select(Photo).order_by(Photo.path)
        if root_path:
            normalized = root_path.rstrip("/")
            stmt = stmt.where(Photo.path.like(normalized + "/%"))

        photos = list(session.scalars(stmt).all())
        if limit is not None:
            photos = photos[:limit]

        hash_groups: dict[str, list[Photo]] = defaultdict(list)
        for photo in photos:
            if photo.checksum_sha256:
                hash_groups[photo.checksum_sha256].append(photo)

        duplicate_ids: set[int] = set()
        keep_ids: set[int] = set()

        # Deterministic rule for exact duplicates:
        # keep the lexicographically first path as the primary copy,
        # route the other identical copies to the duplicate preview tree.
        for items in hash_groups.values():
            if len(items) > 1:
                ordered = sorted(items, key=lambda p: p.path.lower())
                keep_ids.add(ordered[0].id)
                duplicate_ids.update(item.id for item in ordered[1:])

        used_destinations: set[str] = set()
        actions = []
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
                reason = "Exact SHA-256 duplicate; preview routes this extra copy to the duplicate tree."
            else:
                proposed = _normal_destination(photo)
                action = "organize"
                reason = "Primary/unique media; preview organizes by capture year and month."
                if photo.captured_at is None:
                    action = "unknown_date"
                    reason = "No capture date available; preview routes this item to UnknownDate."

            before = proposed
            proposed = _make_unique(proposed, used_destinations)
            collision_resolved = proposed != before
            if collision_resolved:
                counts["name_collisions_resolved"] += 1

            counts[action] += 1
            actions.append({
                "media_id": photo.id,
                "action": action,
                "source": photo.path,
                "proposed_destination": str(proposed),
                "captured_at": photo.captured_at,
                "checksum_sha256": photo.checksum_sha256,
                "exact_duplicate": photo.id in duplicate_ids,
                "primary_duplicate_copy": photo.id in keep_ids,
                "collision_resolved": collision_resolved,
                "reason": reason,
            })

        return {
            "mode": "dry-run",
            "writes_enabled": False,
            "root_filter": root_path,
            "total_actions": len(actions),
            "summary": counts,
            "actions": actions,
        }
