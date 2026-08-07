from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PhotoVault"
    app_version: str = "0.1.0"
    database_path: Path = Path("/data/database/photovault.db")
    config_path: Path = Path("/data/config")
    log_path: Path = Path("/data/logs")
    reports_path: Path = Path("/data/reports")
    storage_path: Path = Path("/storage")
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="PHOTOVAULT_",
        case_sensitive=False,
    )


settings = Settings()
