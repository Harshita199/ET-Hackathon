from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.station import AQIStation
from app.models.aqi_reading import AQIReading


class DashboardService:

    @staticmethod
    def dashboard(db: Session):

        latest = (
            db.query(AQIReading)
            .order_by(AQIReading.timestamp.desc())
            .all()
        )

        station_count = db.query(AQIStation).count()

        city_count = (
            db.query(AQIStation.city)
            .distinct()
            .count()
        )

        avg_aqi = (
            db.query(func.avg(AQIReading.aqi))
            .scalar()
        )

        worst = (
            db.query(
                AQIReading,
                AQIStation
            )
            .join(
                AQIStation,
                AQIReading.station_id == AQIStation.id
            )
            .order_by(AQIReading.aqi.desc())
            .first()
        )

        good = 0
        moderate = 0
        poor = 0
        very_poor = 0
        severe = 0

        latest_per_station = {}

        for reading in latest:

            if reading.station_id not in latest_per_station:
                latest_per_station[reading.station_id] = reading

        for reading in latest_per_station.values():

            if reading.aqi <= 50:
                good += 1

            elif reading.aqi <= 100:
                moderate += 1

            elif reading.aqi <= 200:
                poor += 1

            elif reading.aqi <= 300:
                very_poor += 1

            else:
                severe += 1

        return {

            "total_stations": station_count,

            "cities": city_count,

            "average_aqi": round(avg_aqi or 0, 2),

            "worst_station": (
                worst[1].station_name
                if worst else None
            ),

            "worst_city": (
                worst[1].city
                if worst else None
            ),

            "worst_aqi": (
                round(worst[0].aqi, 2)
                if worst else None
            ),

            "good_air_stations": good,

            "moderate_air_stations": moderate,

            "poor_air_stations": poor,

            "very_poor_air_stations": very_poor,

            "severe_air_stations": severe,

        }

    @staticmethod
    def top_polluted(
        db: Session,
        limit: int = 10
    ):

        rows = (
            db.query(
                AQIReading,
                AQIStation
            )
            .join(
                AQIStation,
                AQIReading.station_id == AQIStation.id
            )
            .order_by(
                AQIReading.aqi.desc()
            )
            .limit(limit)
            .all()
        )

        return [

            {
                "station": station.station_name,
                "city": station.city,
                "aqi": round(reading.aqi, 2)
            }

            for reading, station in rows

        ]

    @staticmethod
    def alerts(db: Session):

        latest = (
            db.query(AQIReading)
            .order_by(AQIReading.timestamp.desc())
            .all()
        )

        station_latest = {}

        for reading in latest:

            if reading.station_id not in station_latest:
                station_latest[reading.station_id] = reading

        alerts = []

        for reading in station_latest.values():

            if reading.aqi < 200:
                continue

            station = (
                db.query(AQIStation)
                .filter(
                    AQIStation.id == reading.station_id
                )
                .first()
            )

            alerts.append({

                "station": station.station_name,

                "city": station.city,

                "aqi": reading.aqi,

                "level": (
                    "SEVERE"
                    if reading.aqi > 300
                    else "VERY_POOR"
                ),

                "message": (
                    "Immediate intervention recommended."
                )

            })

        return alerts

    @staticmethod
    def aqi_trend(
        db: Session,
        station_id: str,
        days: int = 30
    ):

        since = datetime.utcnow() - timedelta(days=days)

        readings = (
            db.query(AQIReading)
            .filter(
                AQIReading.station_id == station_id,
                AQIReading.timestamp >= since
            )
            .order_by(
                AQIReading.timestamp.asc()
            )
            .all()
        )

        return [

            {

                "timestamp": reading.timestamp,

                "aqi": round(reading.aqi, 2)

            }

            for reading in readings

        ]

    @staticmethod
    def city_comparison(db: Session):

        rows = (
            db.query(

                AQIStation.city,

                func.avg(AQIReading.aqi)

            )
            .join(
                AQIReading,
                AQIReading.station_id == AQIStation.id
            )
            .group_by(
                AQIStation.city
            )
            .all()
        )

        return [

            {

                "city": city,

                "average_aqi": round(avg, 2)

            }

            for city, avg in rows

        ]

    @staticmethod
    def city_rankings(db: Session):

        rows = (
            db.query(

                AQIStation.city,

                func.avg(AQIReading.aqi).label("aqi")

            )
            .join(
                AQIReading,
                AQIReading.station_id == AQIStation.id
            )
            .group_by(
                AQIStation.city
            )
            .order_by(
                func.avg(AQIReading.aqi).desc()
            )
            .all()
        )

        rankings = []

        rank = 1

        for city, avg in rows:

            rankings.append({

                "rank": rank,

                "city": city,

                "average_aqi": round(avg, 2)

            })

            rank += 1

        return rankings

    @staticmethod
    def get_summary(db: Session):
    
        data = DashboardService.dashboard(db)
    
        return {
            "stations": data["total_stations"],
            "average_aqi": data["average_aqi"],
            "good": data["good_air_stations"],
            "moderate": data["moderate_air_stations"],
            "poor": data["poor_air_stations"],
            "very_poor": data["very_poor_air_stations"],
            "severe": data["severe_air_stations"],
        }