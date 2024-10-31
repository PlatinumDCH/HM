"""data extraction"""

from typing import Any


class ExchangeRateExtractor:
    def __init__(self, currencies: list[str]):
        self.currencies = currencies

    def extract_rates(self, data: dict[str, Any]) -> dict[str, Any]:
        rates = {}
        for rate in data.get("exchangeRate", []):
            currency = rate.get("currency")
            if currency in self.currencies:
                rates[currency] = {
                    "sale": rate.get("saleRateNB"),
                    "purchase": rate.get("purchaseRateNB"),
                }
        return rates
