from pathlib import Path
from enum import Enum


class DataPath(Enum):
    AUTHORS = Path('data')/'authors.json'
    QUOTES = Path('data')/'quotes.json'
