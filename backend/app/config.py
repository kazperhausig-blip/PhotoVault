from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PhotoVault"
    app_version: str = "0.8.0"

    database_path: Path = Path("/data/database/photovault.db")
    config_path: Path = Path("/data/config")
    log_path: Path = Path("/data/logs")
    reports_path: Path = Path("/data/reports")

    storage_path: Path = Path("/storage")
    scan_root: Path = Path("/storage")
    scan_exclude_paths: str = (
        "/storage/photovault,"
        "/storage/appdata,"
        "/storage/system,"
        "/storage/domains,"
        "/storage/isos"
    )

    # 0.8 photo-archive filter. GIF/BMP/WebP/AVIF/ICO are deliberately
    # excluded by default because they commonly contain web, game or system
    # graphics rather than camera media. Override with PHOTOVAULT_ALLOWED_EXTENSIONS.
    allowed_extensions: str = (
        ".jpg,.jpeg,.png,.tif,.tiff,.heic,.heif,"
        ".cr2,.cr3,.nef,.nrw,.arw,.srf,.sr2,.orf,.rw2,.raf,.dng,.pef,.raw,.rwl,"
        ".3fr,.fff,.iiq,.kdc,.mef,.mos,.mrw,.x3f,"
        ".mp4,.mov,.m4v,.avi,.mkv,.mts,.m2ts,.3gp,.webm,.mpg,.mpeg"
    )

    # Preview destinations are logical output paths only in 0.4.
    # No files are written, moved, renamed or deleted.

    # 0.6 execution output. Docker maps a dedicated Unraid share here as writable.
    output_path: Path = Path("/output")

    organizer_root: Path = Path("/Photos")
    duplicate_root: Path = Path("/Duplicates")
    unknown_date_root: Path = Path("/Photos/UnknownDate")

    hash_chunk_size: int = 4 * 1024 * 1024
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_prefix="PHOTOVAULT_", case_sensitive=False)

    @property
    def excluded_paths(self) -> list[Path]:
        return [Path(x.strip()) for x in self.scan_exclude_paths.split(",") if x.strip()]

    @property
    def archive_extensions(self) -> set[str]:
        from app.scanner.extensions import parse_extension_list
        return parse_extension_list(self.allowed_extensions)


settings = Settings()
