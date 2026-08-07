from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    extension: Mapped[str | None] = mapped_column(String, nullable=True)
    size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    captured_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
    checksum_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    indexed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    media_type: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    camera_make: Mapped[str | None] = mapped_column(String(255), nullable=True)
    camera_model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lens_model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gps_latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    gps_longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    metadata_status: Mapped[str | None] = mapped_column(String(30), nullable=True, index=True)
    metadata_error: Mapped[str | None] = mapped_column(Text, nullable=True)
