from fastapi import APIRouter
from sqlalchemy import func, select

from app.database import SessionLocal
from app.models.photo import Photo
from app.models.scan_job import ScanJob

router = APIRouter(tags=["statistics"])


@router.get("/stats")
def stats() -> dict:
    with SessionLocal() as session:
        total = session.scalar(select(func.count()).select_from(Photo)) or 0
        images = session.scalar(select(func.count()).select_from(Photo).where(Photo.media_type == "image")) or 0
        raw = session.scalar(select(func.count()).select_from(Photo).where(Photo.media_type == "raw")) or 0
        videos = session.scalar(select(func.count()).select_from(Photo).where(Photo.media_type == "video")) or 0
        unknown_dates = session.scalar(select(func.count()).select_from(Photo).where(Photo.captured_at.is_(None))) or 0
        gps_count = session.scalar(
            select(func.count()).select_from(Photo).where(
                Photo.gps_latitude.is_not(None),
                Photo.gps_longitude.is_not(None),
            )
        ) or 0

        duplicate_groups = session.execute(
            select(Photo.checksum_sha256)
            .where(Photo.checksum_sha256.is_not(None))
            .group_by(Photo.checksum_sha256)
            .having(func.count(Photo.id) > 1)
        ).all()

        latest_job = session.scalar(select(ScanJob).order_by(ScanJob.id.desc()).limit(1))

        return {
            "total_media": total,
            "images": images,
            "raw": raw,
            "videos": videos,
            "unknown_capture_dates": unknown_dates,
            "with_gps": gps_count,
            "exact_duplicate_groups": len(duplicate_groups),
            "latest_scan": None if latest_job is None else {
                "job_id": latest_job.id,
                "status": latest_job.status,
                "root_path": latest_job.root_path,
                "started_at": latest_job.started_at,
                "finished_at": latest_job.finished_at,
                "discovered": latest_job.discovered,
                "indexed": latest_job.indexed,
                "skipped_unchanged": latest_job.skipped_unchanged,
                "errors": latest_job.errors,
            },
        }
