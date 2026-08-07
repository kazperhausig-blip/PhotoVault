from fastapi import APIRouter, Query
from sqlalchemy import func, select

from app.database import SessionLocal
from app.models.photo import Photo

router = APIRouter(tags=["duplicates"])


@router.get("/duplicates")
def duplicates(limit: int = Query(default=100, ge=1, le=1000)) -> dict:
    with SessionLocal() as session:
        hashes = session.execute(
            select(Photo.checksum_sha256, func.count(Photo.id).label("count"))
            .where(Photo.checksum_sha256.is_not(None))
            .group_by(Photo.checksum_sha256)
            .having(func.count(Photo.id) > 1)
            .order_by(func.count(Photo.id).desc())
            .limit(limit)
        ).all()

        groups = []
        for checksum, count in hashes:
            items = session.scalars(
                select(Photo)
                .where(Photo.checksum_sha256 == checksum)
                .order_by(Photo.path)
            ).all()

            groups.append({
                "checksum_sha256": checksum,
                "count": count,
                "files": [
                    {
                        "id": item.id,
                        "path": item.path,
                        "filename": item.filename,
                        "size_bytes": item.size_bytes,
                        "captured_at": item.captured_at,
                        "camera_model": item.camera_model,
                    }
                    for item in items
                ],
            })

        return {"duplicate_groups": len(groups), "groups": groups}
