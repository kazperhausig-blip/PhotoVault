import sys
from loguru import logger
from app.config import settings


def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level=settings.log_level, enqueue=True, backtrace=False, diagnose=False)
    return logger
