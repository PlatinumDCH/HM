import asyncio
import sys
from datetime import datetime, timedelta
import json
from config import Currency
from api_client import PrivatBankApiClient
from rate_extractor import ExchangeRateExtractor
from rate_fether import RateFetcher


async def main(days: int, currencies: list[str]):
    api_client = PrivatBankApiClient()
    extractor = ExchangeRateExtractor(currencies)
    fetcher = RateFetcher(api_client, extractor)

    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime("%d.%m.%Y") for i in range(days)]
    tasks = [fetcher.fetch_rate(date) for date in dates]

    results = await asyncio.gather(*tasks)
    print(json.dumps(results, indent=2, ensure_ascii=False))


def get_currencies_from_args(default_currencies):
    currencies = default_currencies.copy()
    if len(sys.argv) > 2:
        dditional_currencies = [arg.upper() for arg in sys.argv[2:]]
        currencies.extend(dditional_currencies)
    return currencies

if __name__ == "__main__":
    days = 1
    default_currencies = [Currency.EUR.value, Currency.USD.value]
    try:
        if len(sys.argv) > 1:
            days = int(sys.argv[1])
            if days < 1 or days > 10:
                raise ValueError("Number of days must be between 1 and 10.")

        currencies = get_currencies_from_args(default_currencies)
    except ValueError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)

    asyncio.run(main(days, currencies))
