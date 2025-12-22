import os

# Конфигурация бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
API_URL = os.getenv("API_URL", "http://price_api:8000/search/v2")

# Валидация
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")
