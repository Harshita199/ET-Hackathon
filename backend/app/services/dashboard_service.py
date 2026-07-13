from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.station import AQIStation
from app.models.aqi_reading import AQIReading


class DashboardService:

    @staticmethod
    def get_summary(db: Session):

        station_count = db.query(AQIStation).count()

        avg_aqi = (
            db.query(func.avg(AQIReading.aqi))
            .scalar()
        )

        good = (
            db.query(AQIReading)
            .filter(AQIReading.aqi <= 50)
            .count()
        )

        moderate = (
            db.query(AQIReading)
            .filter(AQIReading.aqi > 50, AQIReading.aqi <= 100)
            .count()
        )

        poor = (
            db.query(AQIReading)
            .filter(AQIReading.aqi > 100, AQIReading.aqi <= 200)
            .count()
        )

        very_poor = (
            db.query(AQIReading)
            .filter(AQIReading.aqi > 200, AQIReading.aqi <= 300)
            .count()
        )

        severe = (
            db.query(AQIReading)
            .filter(AQIReading.aqi > 300)
            .count()
        )

        return {
            "stations": station_count,
            "average_aqi": round(avg_aqi or 0, 2),
            "good": good,
            "moderate": moderate,
            "poor": poor,
            "very_poor": very_poor,
            "severe": severe,
        }