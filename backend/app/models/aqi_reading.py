from __future__ import annotations

from datetime import datetime
from uuid import UUID

# from sqlalchemy import DateTime, Float, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Float, ForeignKey, UniqueConstraint

from app.models.base_model import BaseModel


class AQIReading(BaseModel):
    __tablename__ = "aqi_readings"

    station_id: Mapped[UUID] = mapped_column(
        ForeignKey("aqi_stations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    aqi: Mapped[float | None] = mapped_column(Float)
    pm25: Mapped[float | None] = mapped_column(Float)
    pm10: Mapped[float | None] = mapped_column(Float)
    no2: Mapped[float | None] = mapped_column(Float)
    so2: Mapped[float | None] = mapped_column(Float)
    co: Mapped[float | None] = mapped_column(Float)
    o3: Mapped[float | None] = mapped_column(Float)

    station: Mapped["AQIStation"] = relationship(
        "AQIStation",
        back_populates="aqi_readings",
    )

    __table_args__ = (
       UniqueConstraint(
        "station_id",
        "timestamp",
        name="uq_station_timestamp",
    ),
)

    # __table_args__ = (
    #     Index("idx_station_timestamp", "station_id", "timestamp"),
    # )