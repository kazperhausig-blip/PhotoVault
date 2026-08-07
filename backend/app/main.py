from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.duplicates import router as duplicates_router
from app.api.health import router as health_router
from app.api.media import router as media_router
from app.api.scan import router as scan_router
from app.api.stats import router as stats_router
from app.config import settings
from app.database import init_database
from app.logging_config import setup_logging

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting {} {}", settings.app_name, settings.app_version)
    settings.config_path.mkdir(parents=True, exist_ok=True)
    settings.log_path.mkdir(parents=True, exist_ok=True)
    settings.reports_path.mkdir(parents=True, exist_ok=True)
    init_database()
    yield
    logger.info("Stopping {}", settings.app_name)


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
app.include_router(health_router)
app.include_router(scan_router)
app.include_router(stats_router)
app.include_router(duplicates_router)
app.include_router(media_router)


@app.get("/", tags=["system"])
def home() -> dict:
    return {
        "name": settings.app_name,
        "status": "running",
        "version": settings.app_version,
        "database": "configured",
        "scanner": "ready",
        "metadata": "enabled",
    }
