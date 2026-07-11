from sqlalchemy import Float, String

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship


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

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
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
    back_populates="station",
    cascade="all, delete-orphan",
)

weather_readings: Mapped[list["WeatherReading"]] = relationship(
    back_populates="station",
    cascade="all, delete-orphan",
)

forecasts: Mapped[list["AQIForecast"]] = relationship(
    back_populates="station",
    cascade="all, delete-orphan",
)

attributions: Mapped[list["SourceAttribution"]] = relationship(
    back_populates="station",
    cascade="all, delete-orphan",
)