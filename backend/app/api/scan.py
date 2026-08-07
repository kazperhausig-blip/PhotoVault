from pathlib import Path
from threading import Thread

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.scanner.service import create_scan_job, run_scan, validate_scan_root
from app.scanner.state import snapshot

router = APIRouter(tags=["scanner"])


class ScanRequest(BaseModel):
    path: str | None = None


@router.post("/scan", status_code=202)
def start_scan(request: ScanRequest | None = None) -> dict:
    current = snapshot()
    if current["running"]:
        raise HTTPException(status_code=409, detail="A scan is already running")

    requested_path = Path(request.path) if request and request.path else None

    try:
        root = validate_scan_root(requested_path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    job_id = create_scan_job(root)
    Thread(target=run_scan, args=(job_id, root), daemon=True, name=f"photovault-scan-{job_id}").start()

    return {"status": "accepted", "job_id": job_id, "root_path": str(root)}


@router.get("/scan/status")
def scan_status() -> dict:
    return snapshot()
