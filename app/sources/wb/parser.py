from typing import List, Dict

def parse_offers(data: dict) -> List[Dict]:
    products = data.get("data", {}).get("products", [])
    offers = []

    for p in products:
        price = p.get("salePriceU")
        if not price:
            continue

        offers.append({
            "title": p.get("name"),
            "price": price / 100,  # WB хранит в копейках
            "url": f"https://www.wildberries.ru/catalog/{p['id']}/detail.aspx"
        })

    return offers
