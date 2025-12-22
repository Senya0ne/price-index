import time
from sqlmodel import Session
from app.sources.ozon.fetch import fetch_search_html
from app.sources.ozon.parser import parse_offers
from app.normalizer.text import normalize_title
from app.core.products import normalize_text, make_canonical_name, get_or_create_product
from app.sources.base import save_price_history
from app.models.offer import Offer

LAST_RUN = 0
MIN_INTERVAL = 600  # 10 минут (Ozon тоже чувствителен)

def fetch_and_save_offers(
    session: Session,
    query: str,
    limit: int = 10
):
    global LAST_RUN

    now = time.time()
    if now - LAST_RUN < MIN_INTERVAL:
        print("Ozon ingestion skipped (cooldown)")
        return

    LAST_RUN = now

    html = fetch_search_html(query)
    if not html:
        return
    
    raw_offers = parse_offers(html)

    for raw in raw_offers[:limit]:
        if not raw.get("price"):
            continue

        title = raw["title"]
        normalized = normalize_text(title)
        
        # Определяем brand и model (пока хардкод для MVP)
        brand = None
        model = None
        
        normalized_lower = normalized.lower()
        if "xiaomi" in normalized_lower:
            brand = "xiaomi"
            if "a27q" in normalized_lower or "redmi a27q" in normalized_lower:
                model = "redmi a27q"
        
        canonical = make_canonical_name(brand, model)
        if not canonical:
            canonical = normalized
        
        product = get_or_create_product(session, normalized, canonical, brand, model)

        offer = Offer(
            product_id=product.id,
            source="ozon",
            price=raw["price"],
            url=raw["url"],
            availability=True
        )

        session.add(offer)

        # Сохраняем историю цен (снапшот по canonical_name)
        save_price_history(
            session,
            product.canonical_name,
            "ozon",
            raw["price"]
        )

    session.commit()
