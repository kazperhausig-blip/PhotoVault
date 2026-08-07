from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PhotoVault"
    app_version: str = "0.6.0"

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


settings = Settings()
