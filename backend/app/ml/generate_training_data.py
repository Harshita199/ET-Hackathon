import random
from datetime import timedelta

from sqlalchemy.orm import Session

# from app.api.dependencies import SessionLocal
from app.database.session import SessionLocal
from app.models.station import AQIStation
from app.models.aqi_reading import AQIReading


def random_variation(value, pct):
    change = value * pct
    return round(random.uniform(value - change, value + change), 2)


def generate_history(db: Session):

    stations = db.query(AQIStation).all()

    print(f"Found {len(stations)} stations")

    total = 0

    for station in stations:

        latest = (
            db.query(AQIReading)
            .filter(AQIReading.station_id == station.id)
            .order_by(AQIReading.timestamp.desc())
            .first()
        )

        if latest is None:
            continue

        base_time = latest.timestamp - timedelta(days=365)

        base_aqi = latest.aqi

        for day in range(365):

            timestamp = base_time + timedelta(days=day)

            seasonal = 15 * (
                (day % 30) / 30
            )

            aqi = max(
                20,
                random_variation(base_aqi + seasonal, 0.12),
            )

            reading = AQIReading(
                station_id=station.id,
                timestamp=timestamp,
                aqi=aqi,
                pm25=max(5, random_variation(aqi * 0.9, 0.15)),
                pm10=max(5, random_variation(aqi * 0.7, 0.15)),
                co=random_variation(5, 0.4),
                no2=random_variation(18, 0.4),
                so2=random_variation(10, 0.4),
                o3=random_variation(25, 0.4),
                temperature=random_variation(30, 0.15),
                humidity=random_variation(55, 0.25),
                pressure=random_variation(1005, 0.02),
                wind_speed=random_variation(2, 0.5),
                wind_direction=random.randint(0, 360),
            )

            db.add(reading)
            total += 1

    db.commit()

    print(f"Inserted {total} readings")


if __name__ == "__main__":

    db = SessionLocal()

    try:
        generate_history(db)
    finally:
        db.close()