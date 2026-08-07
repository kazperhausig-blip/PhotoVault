from threading import Thread

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from app.database import SessionLocal
from app.executor.service import create_job, run_job
from app.executor.state import snapshot
from app.models.copy_job import CopyItem, CopyJob

router = APIRouter(tags=["safe-copy"])


class ExecuteRequest(BaseModel):
    path: str
    exclude: list[str] = []
    confirmation: str


@router.post("/organize/execute", status_code=202)
def execute(request: ExecuteRequest) -> dict:
    if request.confirmation != "COPY_AND_VERIFY":
        raise HTTPException(
            status_code=400,
            detail='Execution requires confirmation exactly equal to "COPY_AND_VERIFY".',
        )
    if snapshot()["running"]:
        raise HTTPException(status_code=409, detail="A copy job is already running")

    job_id = create_job(request.path, request.exclude)
    Thread(target=run_job, args=(job_id,), daemon=True, name=f"photovault-copy-{job_id}").start()
    return {
        "status": "accepted",
        "job_id": job_id,
        "safety": "copy-only; source deletion is not implemented",
    }


@router.get("/organize/execute/status")
def execute_status() -> dict:
    return snapshot()


@router.get("/organize/jobs/{job_id}")
def job_detail(job_id: int) -> dict:
    with SessionLocal() as session:
        job = session.get(CopyJob, job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")

        failed = list(session.scalars(
            select(CopyItem)
            .where(CopyItem.job_id == job_id, CopyItem.status == "failed")
            .order_by(CopyItem.id)
        ).all())

        return {
            "job_id": job.id,
            "status": job.status,
            "source_root": job.source_root,
            "started_at": job.started_at,
            "finished_at": job.finished_at,
            "total": job.total,
            "copied": job.copied,
            "verified": job.verified,
            "skipped_verified": job.skipped_verified,
            "failed": job.failed,
            "error_message": job.error_message,
            "failed_items": [
                {
                    "media_id": x.media_id,
                    "source": x.source,
                    "destination": x.destination,
                    "error": x.error_message,
                }
                for x in failed[:100]
            ],
        }
