import httpx

from app.core.config import settings


class WAQIClient:
    def __init__(self):
        self.base_url = settings.WAQI_BASE_URL
        self.token = settings.WAQI_API_KEY

    async def get_city_data(self, city: str):
        """
        Fetch AQI data for a city.
        Example:
        https://api.waqi.info/feed/delhi/?token=xxxx
        """

        url = f"{self.base_url}/feed/{city}/"

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                url,
                params={
                    "token": self.token
                }
            )

            response.raise_for_status()

            return response.json()