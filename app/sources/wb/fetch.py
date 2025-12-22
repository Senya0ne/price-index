import time
import httpx

WB_API_URL = "https://search.wb.ru/exactmatch/ru/common/v4/search"

def fetch_search_json(query: str) -> dict | None:
    time.sleep(3)  # ⏱️ важно

    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "query": query,
        "resultset": "catalog",
        "sort": "popular",
        "spp": 30,
        "regions": "80",
        "locale": "ru",
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.wildberries.ru/",
    }

    with httpx.Client(headers=headers, timeout=20) as client:
        r = client.get(WB_API_URL, params=params)

        if r.status_code == 429:
            print("WB RATE LIMITED")
            return None

        if r.status_code != 200:
            print(f"Wildberries blocked request: {r.status_code}")
            return None

        return r.json()
