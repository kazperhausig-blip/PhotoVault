from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import ExifTags, Image


DATE_FORMATS = (
    "%Y:%m:%d %H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
)


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bytes):
        try:
            value = value.decode("utf-8", errors="ignore")
        except Exception:
            return None
    text = str(value).strip().strip("\x00")
    return text or None


def _parse_date(value: Any) -> datetime | None:
    text = _clean_text(value)
    if not text:
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    return None


def _rational_to_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        if isinstance(value, tuple) and len(value) == 2 and value[1]:
            return float(value[0]) / float(value[1])
        raise


def _gps_to_decimal(values: Any, ref: str | None) -> float | None:
    if not values or len(values) < 3:
        return None
    try:
        deg = _rational_to_float(values[0])
        minute = _rational_to_float(values[1])
        second = _rational_to_float(values[2])
        result = deg + (minute / 60.0) + (second / 3600.0)
        if ref in {"S", "W"}:
            result = -result
        return result
    except Exception:
        return None


def extract_image_metadata(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "captured_at": None,
        "camera_make": None,
        "camera_model": None,
        "lens_model": None,
        "gps_latitude": None,
        "gps_longitude": None,
        "width": None,
        "height": None,
        "metadata_status": "no_metadata",
        "metadata_error": None,
    }

    try:
        with Image.open(path) as image:
            result["width"], result["height"] = image.size
            exif = image.getexif()

            if not exif:
                result["metadata_status"] = "ok_no_exif"
                return result

            tags = {ExifTags.TAGS.get(tag_id, tag_id): value for tag_id, value in exif.items()}

            result["captured_at"] = (
                _parse_date(tags.get("DateTimeOriginal"))
                or _parse_date(tags.get("DateTimeDigitized"))
                or _parse_date(tags.get("DateTime"))
            )
            result["camera_make"] = _clean_text(tags.get("Make"))
            result["camera_model"] = _clean_text(tags.get("Model"))
            result["lens_model"] = _clean_text(tags.get("LensModel"))

            gps_ifd = None
            try:
                gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
            except Exception:
                gps_ifd = tags.get("GPSInfo")

            if isinstance(gps_ifd, dict):
                gps = {ExifTags.GPSTAGS.get(k, k): v for k, v in gps_ifd.items()}
                lat_ref = _clean_text(gps.get("GPSLatitudeRef"))
                lon_ref = _clean_text(gps.get("GPSLongitudeRef"))
                result["gps_latitude"] = _gps_to_decimal(gps.get("GPSLatitude"), lat_ref)
                result["gps_longitude"] = _gps_to_decimal(gps.get("GPSLongitude"), lon_ref)

            result["metadata_status"] = "ok"
            return result

    except Exception as exc:
        result["metadata_status"] = "error"
        result["metadata_error"] = str(exc)
        return result


def extract_metadata(path: Path, media_type: str) -> dict[str, Any]:
    if media_type == "image":
        return extract_image_metadata(path)

    return {
        "captured_at": None,
        "camera_make": None,
        "camera_model": None,
        "lens_model": None,
        "gps_latitude": None,
        "gps_longitude": None,
        "width": None,
        "height": None,
        "metadata_status": "not_supported_yet",
        "metadata_error": None,
    }
