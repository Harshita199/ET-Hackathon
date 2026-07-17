from sqlalchemy.orm import Session

from app.ingestion.waqi import WAQIClient
from app.services.waqi_parser import WAQIParser
from app.services.station_service import StationService
from app.services.aqi_reading_service import AQIReadingService
from backend.app.services.weather_service import WeatherService


class SyncService:

    @staticmethod
    async def sync_all(cities: list[str], db: Session):

        client = WAQIClient()

        results = []

        for city in cities:

            try:

                payload = await client.get_city_data(city)

                if payload.get("status") != "ok":
                    raise Exception(payload.get("data"))

                station_data = WAQIParser.parse_station(payload)
                reading_data = WAQIParser.parse_reading(payload)
                weather_data = WAQIParser.parse_weather(payload)

                station = StationService.get_or_create(
                    db,
                    station_data,
                )

                AQIReadingService.save(
                    db,
                    station,
                    reading_data,
                )

                WeatherService.save(
                         db,
                         station,
                         weather_data,
                    )

                results.append({
                    "city": city,
                    "status": "success",
                    "aqi": reading_data["aqi"],
                })

                # WeatherService.save(
                #          db,
                #          station,
                #          weather_data,
                #     )

            except Exception as e:

                results.append({
                    "city": city,
                    "status": "failed",
                    "error": str(e),
                })

        return results