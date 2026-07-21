import pandas as pd


class FeatureEngineering:

    @staticmethod
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare dataset for ML training.
        """

        df = df.copy()

        # -------------------------
        # Timestamp Features
        # -------------------------
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        df["year"] = df["timestamp"].dt.year
        df["month"] = df["timestamp"].dt.month
        df["day"] = df["timestamp"].dt.day
        df["hour"] = df["timestamp"].dt.hour
        df["weekday"] = df["timestamp"].dt.weekday

        # -------------------------
        # Sort data
        # -------------------------
        df = df.sort_values(
            ["station_id", "timestamp"]
        )

        # -------------------------
        # Lag Features
        # -------------------------
        df["aqi_lag_1"] = (
            df.groupby("station_id")["aqi"]
            .shift(1)
        )

        df["aqi_lag_2"] = (
            df.groupby("station_id")["aqi"]
            .shift(2)
        )

        df["aqi_lag_3"] = (
            df.groupby("station_id")["aqi"]
            .shift(3)
        )

        # -------------------------
        # Rolling Mean
        # -------------------------
        df["aqi_mean_3"] = (
            df.groupby("station_id")["aqi"]
            .transform(
                lambda x: x.rolling(
                    3,
                    min_periods=1,
                ).mean()
            )
        )

        # -------------------------
        # Target
        # -------------------------
        df["target_aqi"] = (
            df.groupby("station_id")["aqi"]
            .shift(-1)
        )

        # -------------------------
        # Missing Values
        # -------------------------
        numeric_columns = [
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
            "aqi_lag_1",
            "aqi_lag_2",
            "aqi_lag_3",
            "aqi_mean_3",
        ]

        for col in numeric_columns:
            df[col] = df[col].fillna(df[col].median())

        # Remove rows without target
        df = df.dropna(subset=["target_aqi"])

        return df