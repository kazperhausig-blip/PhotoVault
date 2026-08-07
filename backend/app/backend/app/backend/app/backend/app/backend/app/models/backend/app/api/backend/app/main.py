from fastapi import FastAPI

from app.database import init_database
from app.logging_config import setup_logging

from app.api.health import router as health_router


logger = setup_logging()


app = FastAPI(
    title="PhotoVault",
    version="0.1.0"
)


@app.on_event("startup")
def startup():

    logger.info(
        "Starting PhotoVault"
    )

    init_database()


app.include_router(
    health_router
)


@app.get("/")
def home():

    return {
        "name": "PhotoVault",
        "status": "running"
    }
