IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff",
    ".heic", ".heif", ".webp", ".avif",
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

SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | RAW_EXTENSIONS | VIDEO_EXTENSIONS


def media_type_for_extension(extension: str) -> str:
    ext = extension.lower()
    if ext in VIDEO_EXTENSIONS:
        return "video"
    if ext in RAW_EXTENSIONS:
        return "raw"
    return "image"
