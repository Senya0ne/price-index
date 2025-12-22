import httpx
import random

AVITO_SEARCH_URL = "https://www.avito.ru/all"

# Ротация User-Agent для антибана
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
]

def get_headers():
    """Получить заголовки с ротацией User-Agent"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
    }

def fetch_search_html(query: str) -> str | None:
    """Получить HTML поиска с базовым антибаном"""
    params = {
        "q": query,
    }

    headers = get_headers()

    with httpx.Client(headers=headers, timeout=15, follow_redirects=True) as client:
        r = client.get(AVITO_SEARCH_URL, params=params)

        if r.status_code != 200:
            print(f"Avito blocked request: {r.status_code}")
            return None

        return r.text
