from errors import HttpError
from config import APISettings
from typing import Any
import aiohttp  # type: ignore


class PrivatBankApiClient:
    def __init__(self, base_url: str = APISettings.base_url.value):
        self.base_url = base_url

    async def request(self, date: str) -> dict[str, Any]:
        """Get currency exchange rates for a given date"""
        url = f"{self.base_url}{date}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        raise HttpError(f"Error status: {resp.status} for {url}")
            except (
                aiohttp.ClientConnectorError,
                aiohttp.InvalidURL,
                asyncio.TimeoutError,
            ) as err:
                raise HttpError(f"Connection error: {url}", str(err))
