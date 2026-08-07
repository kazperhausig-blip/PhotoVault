from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.photo import Photo

router = APIRouter(tags=["media"])


@router.get("/media/{media_id}")
def media_detail(media_id: int) -> dict:
    with SessionLocal() as session:
        item = session.get(Photo, media_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Media not found")

        return {
            "id": item.id,
            "path": item.path,
            "filename": item.filename,
            "extension": item.extension,
            "media_type": item.media_type,
            "size_bytes": item.size_bytes,
            "checksum_sha256": item.checksum_sha256,
            "captured_at": item.captured_at,
            "modified_at": item.modified_at,
            "camera_make": item.camera_make,
            "camera_model": item.camera_model,
            "lens_model": item.lens_model,
            "gps_latitude": item.gps_latitude,
            "gps_longitude": item.gps_longitude,
            "width": item.width,
            "height": item.height,
            "metadata_status": item.metadata_status,
            "metadata_error": item.metadata_error,
        }
