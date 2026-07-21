from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.station import AQIStation
from app.models.aqi_reading import AQIReading
from datetime import datetime, timedelta


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
            .filter(
                AQIReading.aqi > 50,
                AQIReading.aqi <= 100,
            )
            .count()
        )

        poor = (
            db.query(AQIReading)
            .filter(
                AQIReading.aqi > 100,
                AQIReading.aqi <= 200,
            )
            .count()
        )

        very_poor = (
            db.query(AQIReading)
            .filter(
                AQIReading.aqi > 200,
                AQIReading.aqi <= 300,
            )
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

    @staticmethod
    def get_dashboard(db: Session):

        latest = (
            db.query(AQIReading)
            .order_by(AQIReading.timestamp.desc())
            .first()
        )

        if latest is None:
            return {}

        latest_time = latest.timestamp

        readings = (
            db.query(AQIReading)
            .filter(AQIReading.timestamp == latest_time)
            .all()
        )

        if not readings:
            return {}

        avg = sum(r.aqi for r in readings) / len(readings)

        worst = max(readings, key=lambda x: x.aqi)

        station = (
            db.query(AQIStation)
            .filter(AQIStation.id == worst.station_id)
            .first()
        )

        return {

            "total_stations": db.query(AQIStation).count(),

            "cities": (
                db.query(AQIStation.city)
                .distinct()
                .count()
            ),

            "average_aqi": round(avg, 2),

            "worst_station": station.station_name,

            "worst_city": station.city,

            "worst_aqi": worst.aqi,

            "good_air_stations": sum(
                1 for r in readings if r.aqi <= 50
            ),

            "moderate_air_stations": sum(
                1 for r in readings if 51 <= r.aqi <= 100
            ),

            "poor_air_stations": sum(
                1 for r in readings if r.aqi > 100
            ),
        }

    @staticmethod
    def top_polluted(
        db: Session,
        limit: int = 10,
    ):

        latest = (
            db.query(AQIReading.timestamp)
            .order_by(AQIReading.timestamp.desc())
            .first()
        )

        if latest is None:
            return []

        latest_time = latest[0]

        readings = (
            db.query(AQIReading)
            .filter(
                AQIReading.timestamp == latest_time
            )
            .order_by(AQIReading.aqi.desc())
            .limit(limit)
            .all()
        )

        result = []

        for reading in readings:

            station = (
                db.query(AQIStation)
                .filter(
                    AQIStation.id == reading.station_id
                )
                .first()
            )

            result.append(
                {
                    "station": station.station_name,
                    "city": station.city,
                    "aqi": reading.aqi,
                }
            )

        return result

    @staticmethod
    def alerts(db: Session):

        latest = (
            db.query(AQIReading.timestamp)
            .order_by(AQIReading.timestamp.desc())
            .first()
        )

        if latest is None:
            return []

        latest_time = latest[0]

        readings = (
            db.query(AQIReading)
            .filter(
                AQIReading.timestamp == latest_time,
                AQIReading.aqi > 150,
            )
            .order_by(AQIReading.aqi.desc())
            .all()
        )

        alerts = []

        for reading in readings:

            station = (
                db.query(AQIStation)
                .filter(
                    AQIStation.id == reading.station_id
                )
                .first()
            )

            alerts.append(
                {
                    "station": station.station_name,
                    "city": station.city,
                    "aqi": reading.aqi,
                    "severity": "Critical",
                }
            )

        return alerts

    @staticmethod
    def heatmap(db: Session):

        latest = (
            db.query(AQIReading.timestamp)
            .order_by(AQIReading.timestamp.desc())
            .first()
        )

        if latest is None:
            return []

        latest_time = latest[0]

        readings = (
            db.query(AQIReading)
            .filter(
                AQIReading.timestamp == latest_time
            )
            .all()
        )

        result = []

        for reading in readings:

            station = (
                db.query(AQIStation)
                .filter(
                    AQIStation.id == reading.station_id
                )
                .first()
            )

            result.append(
                {
                    "station": station.station_name,
                    "city": station.city,
                    "lat": station.latitude,
                    "lon": station.longitude,
                    "aqi": reading.aqi,
                }
            )

        return result
    

    @staticmethod
    def aqi_trend(db: Session, station_id: str, days: int = 30):
    
        start_date = datetime.utcnow() - timedelta(days=days)
    
        readings = (
            db.query(AQIReading)
            .filter(
                AQIReading.station_id == station_id,
                AQIReading.timestamp >= start_date
            )
            .order_by(AQIReading.timestamp.asc())
            .all()
        )
    
        return [
            {
                "timestamp": r.timestamp,
                "aqi": r.aqi,
            }
            for r in readings
        ]
