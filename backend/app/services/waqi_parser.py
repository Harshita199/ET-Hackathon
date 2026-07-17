from datetime import datetime


class WAQIParser:
    @staticmethod
    def parse_station(payload: dict) -> dict:
        """
        Parse station information from WAQI response.
        """

        data = payload["data"]
        city = data["city"]

        return {
            "station_code": str(data["idx"]),
            "station_name": city["name"],
            "city": city["name"].split(",")[1].strip() if "," in city["name"] else city["name"],
            "state": city["name"].split(",")[2].strip() if len(city["name"].split(",")) >= 3 else "",
            "latitude": city["geo"][0],
            "longitude": city["geo"][1],
        }

    @staticmethod
    def parse_reading(payload: dict) -> dict:
        """
        Parse AQI + Weather information.
        """

        data = payload["data"]
        iaqi = data.get("iaqi", {})

        def value(key):
            item = iaqi.get(key)
            return item.get("v") if item else None

        return {
            "timestamp": datetime.fromisoformat(data["time"]["iso"]),
            "aqi": data.get("aqi"),
            "pm25": value("pm25"),
            "pm10": value("pm10"),
            "co": value("co"),
            "no2": value("no2"),
            "so2": value("so2"),
            "o3": value("o3"),
            "temperature": value("t"),
            "humidity": value("h"),
            "wind_speed": value("w"),
            "wind_direction": value("wd"),
            "pressure": value("p"),
        }

    @staticmethod
    def parse_forecast(payload: dict) -> dict:
        """
        Parse forecast data.
        We will use this later for comparison with our ML model.
        """

        return payload["data"].get("forecast", {})
    
    @staticmethod
    def parse_weather(payload: dict) -> dict:
    
        data = payload["data"]
        iaqi = data.get("iaqi", {})
    
        def value(key):
            item = iaqi.get(key)
            return item.get("v") if item else None
    
        return {
            "timestamp": datetime.fromisoformat(data["time"]["iso"]),
            "temperature": value("t"),
            "humidity": value("h"),
            "pressure": value("p"),
            "wind_speed": value("w"),
            "wind_direction": value("wd"),
        }