import joblib
import pandas as pd

from pathlib import Path
from sqlalchemy.orm import Session

from app.models.station import AQIStation
from app.models.aqi_reading import AQIReading


class AQIPredictor:

    MODEL_PATH = Path("models/aqi_model.pkl")

    @classmethod
    def load_model(cls):
        return joblib.load(cls.MODEL_PATH)

    @classmethod
    def predict(cls, db: Session, station_id: str):

        model = cls.load_model()

        station = (
            db.query(AQIStation)
            .filter(AQIStation.id == station_id)
            .first()
        )

        if station is None:
            return None

        readings = (
            db.query(AQIReading)
            .filter(AQIReading.station_id == station_id)
            .order_by(AQIReading.timestamp.desc())
            .limit(3)
            .all()
        )

        if len(readings) < 3:
            return None

        latest = readings[0]

        df = pd.DataFrame(
            [
                {
                    # Location Features
                    "latitude": station.latitude,
                    "longitude": station.longitude,

                    # Pollution Features
                    "pm25": latest.pm25,
                    "pm10": latest.pm10,
                    "co": latest.co,
                    "no2": latest.no2,
                    "so2": latest.so2,
                    "o3": latest.o3,

                    # Weather Features
                    "temperature": latest.temperature,
                    "humidity": latest.humidity,
                    "pressure": latest.pressure,
                    "wind_speed": latest.wind_speed,
                    "wind_direction": latest.wind_direction,

                    # Time Features
                    "year": latest.timestamp.year,
                    "month": latest.timestamp.month,
                    "day": latest.timestamp.day,
                    "hour": latest.timestamp.hour,
                    "weekday": latest.timestamp.weekday(),

                    # Historical AQI Features
                    "aqi_lag_1": readings[0].aqi,
                    "aqi_lag_2": readings[1].aqi,
                    "aqi_lag_3": readings[2].aqi,
                    "aqi_mean_3": (
                        readings[0].aqi
                        + readings[1].aqi
                        + readings[2].aqi
                    ) / 3,
                }
            ]
        )

        # Fill missing numeric values
        df = df.fillna(df.median(numeric_only=True))

        # Ensure feature order matches training
        features = [
            "latitude",
            "longitude",
            "pm25",
            "pm10",
            "co",
            "no2",
            "so2",
            "o3",
            "temperature",
            "humidity",
            "pressure",
            "wind_speed",
            "wind_direction",
            "year",
            "month",
            "day",
            "hour",
            "weekday",
            "aqi_lag_1",
            "aqi_lag_2",
            "aqi_lag_3",
            "aqi_mean_3",
        ]

        df = df[features]

        prediction = model.predict(df)[0]

        return {
            "station": station.station_name,
            "city": station.city,
            "current_aqi": latest.aqi,
            "predicted_aqi": round(float(prediction), 2),
            "prediction_for": "Next Reading",
        }