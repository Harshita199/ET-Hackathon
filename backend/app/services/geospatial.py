from sqlalchemy.orm import Session

from app.models.station import AQIStation
from app.models.aqi_reading import AQIReading


class GeospatialService:

    @staticmethod
    def hotspots(db: Session):

        stations = db.query(AQIStation).all()

        hotspots = []

        for station in stations:

            latest = (
                db.query(AQIReading)
                .filter(
                    AQIReading.station_id == station.id
                )
                .order_by(
                    AQIReading.timestamp.desc()
                )
                .first()
            )

            if latest is None:
                continue

            if latest.aqi <= 50:
                category = "Good"
                color = "green"

            elif latest.aqi <= 100:
                category = "Moderate"
                color = "yellow"

            elif latest.aqi <= 200:
                category = "Poor"
                color = "orange"

            elif latest.aqi <= 300:
                category = "Very Poor"
                color = "red"

            else:
                category = "Severe"
                color = "purple"

            hotspots.append({

                "station_id": station.id,

                "station": station.station_name,

                "city": station.city,

                "latitude": station.latitude,

                "longitude": station.longitude,

                "aqi": round(latest.aqi, 2),

                "category": category,

                "marker_color": color,

                "last_updated": latest.timestamp

            })

        return hotspots