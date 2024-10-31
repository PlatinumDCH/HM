"""data extraction"""

from typing import Any, List, Dict


class ExchangeRateExtractor:
    def __init__(self, currencies: List[str]):
        self.currencies = currencies

    def extract_rates(self, data: dict[str, Any]) -> Dict[str, Any]:
        rates = {}
        for rate in data.get("exchangeRate", []):
            currency = rate.get("currency")
            if currency in self.currencies:
                rates[currency] = {
                    "sale": rate.get("saleRateNB"),
                    "purchase": rate.get("purchaseRateNB"),
                }
        return rates
