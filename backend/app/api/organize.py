from fastapi import APIRouter, Query

from app.organizer.preview import build_preview

router = APIRouter(tags=["organizer"])


@router.get("/organize/preview")
def organizer_preview(
    path: str | None = Query(default=None, description="Optional scanned source root, e.g. /storage/disk_1/Backup/Billeder"),
    limit: int | None = Query(default=None, ge=1, le=50000),
) -> dict:
    return build_preview(root_path=path, limit=limit)
