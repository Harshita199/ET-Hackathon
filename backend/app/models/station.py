from __future__ import annotations

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class AQIStation(BaseModel):
    __tablename__ = "aqi_stations"

    station_code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    station_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    aqi_readings: Mapped[list["AQIReading"]] = relationship(
        "AQIReading",
        back_populates="station",
        cascade="all, delete-orphan",
    )