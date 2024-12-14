from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_FOLDER = BASE_DIR / 'templates'

print(TEMPLATE_FOLDER)
print(TEMPLATE_FOLDER.exists())
