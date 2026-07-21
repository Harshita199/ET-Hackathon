import joblib
import numpy as np
import pandas as pd

from pathlib import Path
from sqlalchemy.orm import Session

from app.models.station import AQIStation
from app.models.aqi_reading import AQIReading
from app.ml.insights import AQIInsights


class AQIPredictor:

    MODEL_PATH = Path("models/aqi_model.pkl")

    FEATURES = [
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
            return {
                "error": "Station not found"
            }

        readings = (
            db.query(AQIReading)
            .filter(AQIReading.station_id == station_id)
            .order_by(AQIReading.timestamp.desc())
            .limit(3)
            .all()
        )

        if len(readings) < 3:
            return {
                "error": "Not enough historical readings"
            }

        latest = readings[0]

        data = {
            # Location
            "latitude": station.latitude,
            "longitude": station.longitude,

            # Pollutants
            "pm25": latest.pm25,
            "pm10": latest.pm10,
            "co": latest.co,
            "no2": latest.no2,
            "so2": latest.so2,
            "o3": latest.o3,

            # Weather
            "temperature": latest.temperature,
            "humidity": latest.humidity,
            "pressure": latest.pressure,
            "wind_speed": latest.wind_speed,
            "wind_direction": latest.wind_direction,

            # Time
            "year": latest.timestamp.year,
            "month": latest.timestamp.month,
            "day": latest.timestamp.day,
            "hour": latest.timestamp.hour,
            "weekday": latest.timestamp.weekday(),

            # Historical AQI
            "aqi_lag_1": readings[0].aqi,
            "aqi_lag_2": readings[1].aqi,
            "aqi_lag_3": readings[2].aqi,
            "aqi_mean_3": (
                readings[0].aqi +
                readings[1].aqi +
                readings[2].aqi
            ) / 3,
        }

        df = pd.DataFrame([data])

        df = df.fillna(df.median(numeric_only=True))

        df = df[cls.FEATURES]

        prediction = float(model.predict(df)[0])

        tree_predictions = [
            tree.predict(df)[0]
            for tree in model.estimators_
        ]

        std = np.std(tree_predictions)

        confidence = round(
            max(50, 100 - std),
            2
        )

        insight = AQIInsights.generate(
            latest.aqi,
            prediction
        )

        return {
            "station": station.station_name,
            "city": station.city,
            "current_aqi": round(float(latest.aqi), 2),
            "predicted_aqi": round(prediction, 2),
            "confidence": confidence,
            "prediction_for": "Next Reading",
            "category": insight["category"],
            "trend": insight["trend"],
            "health_advice": insight["health_advice"],
        }