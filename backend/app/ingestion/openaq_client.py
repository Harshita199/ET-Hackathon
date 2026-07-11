import httpx

from app.core.config import settings


class OpenAQClient:
    def __init__(self):
        self.base_url = settings.OPENAQ_BASE_URL

    async def get_locations(self):
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{self.base_url}/locations",
                params={
                    "limit": 10,
                },
            )

            response.raise_for_status()

            return response.json()