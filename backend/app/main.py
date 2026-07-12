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


@app.post("/test/save-station")
async def save_station(
    city: str = "delhi",
    db: Session = Depends(get_db),
):

    client = WAQIClient()

    data = await client.get_city_data(city)
    
    parsed = parse_waqi_response(data)
    
    station = StationService.save(
        db,
        parsed["station"],
    )
    
    reading = AQIReadingService.save(
        db,
        station,
        parsed["reading"],
    )
    
    return {
        "message": "Data synced successfully",
        "station": station.station_name,
        "aqi": reading.aqi,
        "timestamp": reading.timestamp,
    }