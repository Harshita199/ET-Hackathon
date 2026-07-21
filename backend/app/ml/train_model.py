import joblib

from sklearn.ensemble import RandomForestRegressor

from app.ml.dataset_builder import DatasetBuilder
from app.ml.feature_engineering import FeatureEngineering


class AQIModelTrainer:

    MODEL_PATH = "models/aqi_model.pkl"

    @staticmethod
    def train(db):

        # -------------------------
        # Build Dataset
        # -------------------------
        df = DatasetBuilder.build(db)

        df = FeatureEngineering.transform(df)

        if len(df) < 5:
            return {
                "status": "failed",
                "message": "Not enough training data.",
                "records": len(df),
            }

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

        X = df[features]

        y = df["target_aqi"]

        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
        )

        model.fit(X, y)

        joblib.dump(model, AQIModelTrainer.MODEL_PATH)

        return {
            "status": "success",
            "records": len(df),
            "model_path": AQIModelTrainer.MODEL_PATH,
        }