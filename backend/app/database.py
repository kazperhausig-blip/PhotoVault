
from pathlib import Path
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings

class Base(DeclarativeBase):
    pass

Path(settings.database_path).parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite:///{settings.database_path}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def _migrate_photos_table() -> None:
    inspector = inspect(engine)
    if "photos" not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns("photos")}
    migrations = {
        "modified_at": "ALTER TABLE photos ADD COLUMN modified_at DATETIME",
        "media_type": "ALTER TABLE photos ADD COLUMN media_type VARCHAR(20)",
        "last_seen_at": "ALTER TABLE photos ADD COLUMN last_seen_at DATETIME",
    }
    with engine.begin() as connection:
        for column, sql in migrations.items():
            if column not in existing:
                connection.execute(text(sql))

def init_database() -> None:
    from app.models.photo import Photo  # noqa: F401
    from app.models.scan_job import ScanJob  # noqa: F401
    Base.metadata.create_all(bind=engine)
    _migrate_photos_table()

def database_is_healthy() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
