from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.station import AQIStation
from app.models.aqi_reading import AQIReading


class StationQueryService:

    @staticmethod
    def get_all(db: Session):

        latest = (
            db.query(
                AQIReading.station_id,
                func.max(AQIReading.timestamp).label("latest_time"),
            )
            .group_by(AQIReading.station_id)
            .subquery()
        )

        rows = (
            db.query(
                AQIStation.id,
                AQIStation.station_code,
                AQIStation.station_name,
                AQIStation.city,
                AQIStation.state,
                AQIStation.latitude,
                AQIStation.longitude,
                AQIReading.aqi,
                AQIReading.timestamp,
            )
            .join(
                latest,
                AQIStation.id == latest.c.station_id,
            )
            .join(
                AQIReading,
                (AQIReading.station_id == latest.c.station_id)
                & (AQIReading.timestamp == latest.c.latest_time),
            )
            .order_by(AQIStation.city)
            .all()
        )

        return [
            {
                "id": row.id,
                "station_code": row.station_code,
                "station_name": row.station_name,
                "city": row.city,
                "state": row.state,
                "latitude": row.latitude,
                "longitude": row.longitude,
                "aqi": row.aqi,
                "timestamp": row.timestamp,
            }
            for row in rows
        ]