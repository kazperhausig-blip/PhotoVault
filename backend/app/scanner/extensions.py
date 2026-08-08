PHOTO_IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic", ".heif",
}

# These are technically images, but are intentionally NOT part of the default
# photo archive profile because they are commonly web/system/game graphics.
NON_PHOTO_IMAGE_EXTENSIONS = {
    ".gif", ".bmp", ".webp", ".avif", ".ico",
}

RAW_EXTENSIONS = {
    ".cr2", ".cr3", ".nef", ".nrw", ".arw", ".srf", ".sr2",
    ".orf", ".rw2", ".raf", ".dng", ".pef", ".raw", ".rwl",
    ".3fr", ".fff", ".iiq", ".kdc", ".mef", ".mos", ".mrw", ".x3f",
}

VIDEO_EXTENSIONS = {
    ".mp4", ".mov", ".m4v", ".avi", ".mkv", ".mts", ".m2ts",
    ".3gp", ".webm", ".mpg", ".mpeg",
}

DEFAULT_ARCHIVE_EXTENSIONS = PHOTO_IMAGE_EXTENSIONS | RAW_EXTENSIONS | VIDEO_EXTENSIONS


def parse_extension_list(value: str) -> set[str]:
    result: set[str] = set()
    for item in value.split(","):
        item = item.strip().lower()
        if not item:
            continue
        if not item.startswith("."):
            item = "." + item
        result.add(item)
    return result


def media_type_for_extension(extension: str) -> str:
    ext = extension.lower()
    if ext in VIDEO_EXTENSIONS:
        return "video"
    if ext in RAW_EXTENSIONS:
        return "raw"
    return "image"
