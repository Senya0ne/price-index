import httpx

BASE_URL = "https://www.ozon.ru/search/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9",
}

def fetch_search_html(query: str) -> str | None:
    params = {
        "text": query,
        "from_global": "true",
    }

    with httpx.Client(headers=HEADERS, timeout=10, follow_redirects=True) as client:
        r = client.get(BASE_URL, params=params)

        if r.status_code != 200:
            print(f"Ozon blocked request: {r.status_code}")
            return None

        return r.text
