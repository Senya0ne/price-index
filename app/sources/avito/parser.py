from bs4 import BeautifulSoup
from typing import List, Dict

def parse_offers(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")
    offers = []

    items = soup.select('div[data-marker="item"]')

    for item in items:
        title_el = item.select_one('[itemprop="name"]')
        price_el = item.select_one('[itemprop="price"]')
        link_el = item.select_one('a[data-marker="item-title"]')

        if not title_el or not price_el or not link_el:
            continue

        title = title_el.get_text(strip=True)
        price = price_el.get("content")
        url = link_el.get("href")

        if not price or not url:
            continue

        offers.append({
            "title": title,
            "price": float(price),
            "url": f"https://www.avito.ru{url}",
        })

    return offers
