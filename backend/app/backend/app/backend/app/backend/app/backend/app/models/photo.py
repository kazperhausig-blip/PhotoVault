from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class Photo(Base):

    __tablename__ = "photos"

    id = Column(
        Integer,
        primary_key=True
    )

    path = Column(
        String,
        unique=True,
        nullable=False
    )

    filename = Column(
        String
    )

    created_at = Column(
        DateTime
    )

    checksum = Column(
        String
    )
