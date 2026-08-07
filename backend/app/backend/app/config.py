from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "PhotoVault"

    database_path: Path = Path("/database/photovault.db")

    photo_path: Path = Path("/photos")

    log_level: str = "INFO"


settings = Settings()
