from fastapi import APIRouter

from app.config import settings
from app.scanner.extensions import NON_PHOTO_IMAGE_EXTENSIONS

router = APIRouter(tags=["system"])


@router.get("/filter/config")
def filter_config() -> dict:
    return {
        "mode": "photo-archive",
        "allowed_extensions": sorted(settings.archive_extensions),
        "blocked_common_graphics": sorted(NON_PHOTO_IMAGE_EXTENSIONS),
        "fixed_excluded_paths": [str(path) for path in settings.excluded_paths],
        "note": "Request-level exclusions can still be added; fixed exclusions always apply during scanning.",
    }
