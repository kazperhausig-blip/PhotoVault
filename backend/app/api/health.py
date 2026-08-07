
from fastapi import APIRouter
from app.config import settings
from app.database import database_is_healthy
router = APIRouter(tags=["system"])

@router.get("/health")
def health() -> dict:
    ok = database_is_healthy()
    return {"status": "ok" if ok else "degraded", "service": settings.app_name, "version": settings.app_version, "database": "ok" if ok else "error", "scanner": "ready", "storage_mode": "read-only"}
