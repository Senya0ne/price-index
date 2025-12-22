from bs4 import BeautifulSoup
from typing import List, Dict

def parse_offers(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")

    offers = []

    for item in soup.select("div[data-widget='searchResultsV2'] a"):
        title = item.get_text(strip=True)
        href = item.get("href")

        if not title or not href:
            continue

        # Цена может быть не всегда
        price_el = item.find("span")
        price = None
        if price_el:
            digits = "".join(c for c in price_el.get_text() if c.isdigit())
            if digits:
                price = float(digits)

        offers.append({
            "title": title,
            "price": price,
            "url": "https://www.ozon.ru" + href
        })

    return offers
