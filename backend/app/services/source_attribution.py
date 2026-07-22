from sqlalchemy.orm import Session

from app.models.station import AQIStation
from app.models.aqi_reading import AQIReading


class SourceAttributionService:

    @staticmethod
    def analyze(db: Session, station_id: str):

        station = (
            db.query(AQIStation)
            .filter(AQIStation.id == station_id)
            .first()
        )

        if not station:
            return None

        reading = (
            db.query(AQIReading)
            .filter(AQIReading.station_id == station_id)
            .order_by(AQIReading.timestamp.desc())
            .first()
        )

        if not reading:
            return None

        traffic = 20
        construction = 20
        industry = 20
        other = 10

        # Traffic contribution
        if reading.no2:
            if reading.no2 > 80:
                traffic += 30
            elif reading.no2 > 40:
                traffic += 20
            else:
                traffic += 10

        if reading.co:
            if reading.co > 2:
                traffic += 10

        # Construction
        if reading.pm10:
            if reading.pm10 > 180:
                construction += 35
            elif reading.pm10 > 100:
                construction += 20
            else:
                construction += 10

        # Industry
        if reading.so2:
            if reading.so2 > 40:
                industry += 30
            elif reading.so2 > 20:
                industry += 15

        if reading.o3:
            if reading.o3 > 100:
                other += 20

        total = traffic + construction + industry + other

        traffic = round(traffic * 100 / total, 1)
        construction = round(construction * 100 / total, 1)
        industry = round(industry * 100 / total, 1)
        other = round(other * 100 / total, 1)

        confidence = min(
            95,
            70 + (reading.aqi / 10)
        )

        return {
            "station": station.station_name,
            "city": station.city,
            "traffic": traffic,
            "construction": construction,
            "industry": industry,
            "other": other,
            "confidence": round(confidence, 1)
        }