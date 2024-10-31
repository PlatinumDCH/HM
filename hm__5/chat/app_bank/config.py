from enum import Enum


class APISettings(Enum):
    base_url = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

class Currency(Enum):
    EUR = "EUR"
    USD = "USD"