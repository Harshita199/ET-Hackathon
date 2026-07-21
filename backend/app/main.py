from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/health/db")
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "database": "connected"
    }

from app.ingestion.openaq_client import OpenAQClient

@app.get("/test/openaq")
async def test_openaq():

    client = OpenAQClient()

    data = await client.get_locations()

    return data

from app.ingestion.waqi import WAQIClient


@app.get("/test/waqi")
async def test_waqi():

    client = WAQIClient()

    return await client.get_city_data("delhi")

from app.ingestion.waqi import WAQIClient
from app.services.waqi_parser import WAQIParser


@app.get("/test/parser")
async def test_parser(city: str = "delhi"):

    client = WAQIClient()

    payload = await client.get_city_data(city)

    station = WAQIParser.parse_station(payload)
    reading = WAQIParser.parse_reading(payload)

    return {
        "station": station,
        "reading": reading,
    }

from sqlalchemy.orm import Session
from fastapi import Depends

from app.api.dependencies import get_db

from app.ingestion.waqi import WAQIClient
from app.services.waqi_parser import WAQIParser
from app.services.station_service import StationService
from app.services.aqi_reading_service import AQIReadingService

@app.post("/test/save-station")
async def save_station(
    city: str = "delhi",
    db: Session = Depends(get_db),
):

    client = WAQIClient()

    data = await client.get_city_data(city)
    
    # parsed = parse_waqi_response(data)
    station_data = WAQIParser.parse_station(data)
    reading_data = WAQIParser.parse_reading(data)
    
    station = StationService.get_or_create(
       db,
       station_data,
    )
    
    reading = AQIReadingService.save(
      db,
      station,
      reading_data,
)
    
    # return {
    #     "message": "Data synced successfully",
    #     "station": station.station_name,
    #     "aqi": reading.aqi,
    #     "timestamp": reading.timestamp,
    # }
    return {
      "message": "Data synced successfully",
      "station": station.station_name,
      "aqi": reading.aqi,
      "timestamp": reading.timestamp,
}

from app.ingestion.cities import DEFAULT_CITIES
from app.services.sync_service import SyncService
@app.post("/sync")
async def sync_all(
    db: Session = Depends(get_db),
):

    results = await SyncService.sync_all(
        DEFAULT_CITIES,
        db,
    )

    return {
        "total": len(results),
        "success": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] == "failed"]),
        "results": results,
    }

# @app.get("/stations")
# def get_stations(
#     db: Session = Depends(get_db),
# ):

#     stations = StationService.get_all(db)

#     return [
#         {
#             "id": str(station.id),
#             "station_code": station.station_code,
#             "station_name": station.station_name,
#             "city": station.city,
#             "state": station.state,
#             "latitude": station.latitude,
#             "longitude": station.longitude,
#         }
#         for station in stations
#     ]



@app.get("/stations/{station_id}/history")
def station_history(
    station_id: str,
    db: Session = Depends(get_db),
):

    readings = AQIReadingService.get_history(
        db,
        station_id,
    )

    return [
        {
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
            "wind_speed": reading.wind_speed,
            "pressure": reading.pressure,
        }
        for reading in readings
    ]

from app.services.dashboard_service import DashboardService
@app.get("/summary")
def summary(
    db: Session = Depends(get_db),
):
    return DashboardService.get_summary(db)



from app.services.station_query_service import StationQueryService
@app.get("/stations")
def get_stations(
    db: Session = Depends(get_db),
):
    return StationQueryService.get_all(db)

from app.ml.dataset_builder import DatasetBuilder
# @app.get("/ml/dataset")
# def ml_dataset(
#     db: Session = Depends(get_db),
# ):

#     df = DatasetBuilder.build(db)

#     return df.to_dict(orient="records")
from fastapi.encoders import jsonable_encoder
import pandas as pd
import numpy as np

@app.get("/ml/dataset")
def dataset(db: Session = Depends(get_db)):
    df = DatasetBuilder.build(db)

    # Convert all NaN/Inf to None
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    records = df.to_dict(orient="records")

    # FastAPI-safe JSON encoding
    return jsonable_encoder(records)

from fastapi.encoders import jsonable_encoder
import pandas as pd
from app.ml.feature_engineering import FeatureEngineering
import numpy as np

@app.get("/ml/features")
def features(db: Session = Depends(get_db)):
    df = DatasetBuilder.build(db)

    # your feature engineering
    feature_df = FeatureEngineering.transform(df)

    # IMPORTANT: make JSON safe
    feature_df = feature_df.replace([np.inf, -np.inf], np.nan)
    feature_df = feature_df.astype(object)
    feature_df = feature_df.where(pd.notnull(feature_df), None)

    records = feature_df.to_dict(orient="records")

    return jsonable_encoder(records)

from app.ml.train_model import AQIModelTrainer


@app.post("/ml/train")
def train_model(
    db: Session = Depends(get_db),
):
    return AQIModelTrainer.train(db)

from app.ml.predictor import AQIPredictor
@app.get("/ml/predict/{station_id}")
def predict(
    station_id: str,
    db: Session = Depends(get_db),
):

    result = AQIPredictor.predict(
        db,
        station_id,
    )

    if result is None:
        return {
            "status": "failed",
            "message": "Not enough data for prediction."
        }

    return result

from app.models.aqi_reading import AQIReading


@app.get("/ml/history/{station_id}")
def history(station_id: str, db: Session = Depends(get_db)):

    readings = (
        db.query(AQIReading)
        .filter(AQIReading.station_id == station_id)
        .order_by(AQIReading.timestamp.asc())
        .all()
    )

    return [
        {
            "timestamp": r.timestamp,
            "aqi": r.aqi
        }
        for r in readings
    ]


@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    return DashboardService.get_dashboard(db)

@app.get("/alerts")
def alerts(db: Session = Depends(get_db)):
    return DashboardService.alerts(db)

@app.get("/top-polluted")
def top_polluted(db: Session = Depends(get_db)):
    return DashboardService.top_polluted(db)

@app.get("/aqi-trend")
def aqi_trend(
    station_id: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    return DashboardService.aqi_trend(
        db,
        station_id,
        days,
    )