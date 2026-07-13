from sqlalchemy.orm import Session

from app.models.aqi_reading import AQIReading


class AQIReadingService:

    @staticmethod
    def get_by_station_and_timestamp(
        db: Session,
        station_id,
        timestamp,
    ):
        return (
            db.query(AQIReading)
            .filter(
                AQIReading.station_id == station_id,
                AQIReading.timestamp == timestamp,
            )
            .first()
        )

    @staticmethod
    def save(
        db: Session,
        station,
        reading_data: dict,
    ):

        existing = AQIReadingService.get_by_station_and_timestamp(
            db,
            station.id,
            reading_data["timestamp"],
        )

        if existing:
            return existing

        reading = AQIReading(
            station_id=station.id,
            **reading_data,
        )

        db.add(reading)
        db.commit()
        db.refresh(reading)

        return reading

    @staticmethod
    def get_history(db: Session, station_id: str, limit: int = 100):
    
        return (
            db.query(AQIReading)
            .filter(AQIReading.station_id == station_id)
            .order_by(AQIReading.timestamp.desc())
            .limit(limit)
            .all()
        )