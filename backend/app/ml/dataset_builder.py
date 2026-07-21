
import pandas as pd
import numpy as np

from sqlalchemy.orm import Session

from app.models.station import AQIStation
from app.models.aqi_reading import AQIReading

class DatasetBuilder:

    @staticmethod
    def build(db: Session) -> pd.DataFrame:

        rows = (
            db.query(AQIReading, AQIStation)
            .join(AQIStation, AQIReading.station_id == AQIStation.id)
            .order_by(AQIReading.timestamp.asc())
            .all()
        )

        dataset = []

        for reading, station in rows:
            dataset.append(
                {
                    "station_id": str(station.id),
                    "station_code": station.station_code,
                    "station_name": station.station_name,
                    "city": station.city,
                    "state": station.state,
                    "latitude": station.latitude,
                    "longitude": station.longitude,
                    "timestamp": reading.timestamp,
                    "aqi": reading.aqi,
                    "pm25": reading.pm25,
                    "pm10": reading.pm10,
                    "co": reading.co,
                    "no2": reading.no2,
                    "so2": reading.so2,
                    "o3": reading.o3,
                    "temperature": reading.temperature,
                    "humidity": reading.humidity,
                    "pressure": reading.pressure,
                    "wind_speed": reading.wind_speed,
                    "wind_direction": reading.wind_direction,
                }
            )

        df = pd.DataFrame(dataset)

        print("\nMissing values:")
        print(df.isna().sum())

        print("\nInfinity values:")
        print(np.isinf(df.select_dtypes(include="number")).sum())

        # IMPORTANT FIX
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.where(pd.notnull(df), None)

        return df