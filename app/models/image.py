from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.sql import func


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    file_path: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False,
        index=True,
    )
    attempts: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    metadata_record: Mapped["ImageMetadata | None"] = relationship(
        "ImageMetadata",
        back_populates="image",
        uselist=False,
        cascade="all, delete-orphan",
    )


class ImageMetadata(Base):
    __tablename__ = "image_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    subject: Mapped[str] = mapped_column(String(100), index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    attributes: Mapped[list[str]] = mapped_column(JSONB)
    caption: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float)
    model_name: Mapped[str] = mapped_column(String(100))
    raw_response: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    image: Mapped[Image] = relationship(
        "Image",
        back_populates="metadata_record",
    )

class AICallLog(Base):
    __tablename__ = "ai_call_logs"

    id = Column(Integer, primary_key=True)

    image_id = Column(
        Integer,
        ForeignKey("images.id"),
        nullable=False,
    )

    provider = Column(String(50), nullable=False)
    model_name = Column(String(100), nullable=False)

    status = Column(String(30), nullable=False)

    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)

    estimated_cost_usd = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    error_message = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )