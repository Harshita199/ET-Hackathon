from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Float, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class WeatherReading(BaseModel):
    __tablename__ = "weather_readings"

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

    temperature: Mapped[float | None] = mapped_column(Float)
    humidity: Mapped[float | None] = mapped_column(Float)
    pressure: Mapped[float | None] = mapped_column(Float)
    wind_speed: Mapped[float | None] = mapped_column(Float)
    wind_direction: Mapped[float | None] = mapped_column(Float)

    station: Mapped["AQIStation"] = relationship(
        "AQIStation",
        back_populates="weather_readings",
    )

    __table_args__ = (
        Index(
            "idx_weather_station_timestamp",
            "station_id",
            "timestamp",
        ),
    )