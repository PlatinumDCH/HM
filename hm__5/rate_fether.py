"""logic get course for specific date"""

import asyncio
from typing import Any
from api_client import PrivatBankApiClient
from rate_extractor import ExchangeRateExtractor
from errors import HttpError


class RateFetcher:
    def __init__(
        self, api_client: PrivatBankApiClient, extractor: ExchangeRateExtractor
    ):
        self.api_client = api_client
        self.extractor = extractor

    async def fetch_rate(self, date: str) -> dict[str, Any]:
        try:
            data = await self.api_client.request(date)
            rates = self.extractor.extract_rates(data)
            return {date: rates}
        except HttpError as e:
            print(f"Failed to fetch rates for {date}: {e}")
            return {date: None}
