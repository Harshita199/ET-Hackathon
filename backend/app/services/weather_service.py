from sqlalchemy.orm import Session

from app.models.weather import WeatherReading


class WeatherService:

    @staticmethod
    def save(db: Session, station, weather_data: dict):

        existing = (
            db.query(WeatherReading)
            .filter(
                WeatherReading.station_id == station.id,
                WeatherReading.timestamp == weather_data["timestamp"],
            )
            .first()
        )

        if existing:
            return existing

        weather = WeatherReading(
            station_id=station.id,
            **weather_data,
        )

        db.add(weather)
        db.commit()
        db.refresh(weather)

        return weather

    @staticmethod
    def get_latest(db: Session, station_id):

        return (
            db.query(WeatherReading)
            .filter(
                WeatherReading.station_id == station_id,
            )
            .order_by(
                WeatherReading.timestamp.desc()
            )
            .first()
        )