from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.product import Product
from app.models.offer import Offer

router = APIRouter(prefix="/search")

@router.get("/")
def search(q: str, session: Session = Depends(get_session)):
    products = session.exec(
        select(Product).where(Product.normalized_name.contains(q))
    ).all()

    results = []
    for p in products:
        offers = session.exec(
            select(Offer).where(Offer.product_id == p.id)
        ).all()

        results.append({
            "product": p.normalized_name,
            "offers": offers
        })

    return results

@router.get("/v2")
def search_v2(q: str, session: Session = Depends(get_session)):
    """Продуктовый поиск: группировка офферов, лучшая цена, источники"""
    # Получаем все продукты, которые подходят под запрос (ищем по canonical_name)
    products = session.exec(
        select(Product).where(Product.canonical_name.contains(q.lower()))
    ).all()
    
    # Если не нашли по canonical_name, ищем по normalized_name
    if not products:
        products = session.exec(
            select(Product).where(Product.normalized_name.contains(q.lower()))
        ).all()

    if not products:
        return {
            "query": q,
            "results": []
        }

    product_ids = tuple(p.id for p in products)

    # Получаем все офферы для этих продуктов
    offers = session.exec(
        select(Offer).where(Offer.product_id.in_(product_ids))
    ).all()

    # Создаем мапу product_id -> product для быстрого доступа
    products_map = {p.id: p for p in products}

    # Группируем по canonical_name
    grouped = {}

    for offer in offers:
        product = products_map[offer.product_id]
        # Используем canonical_name для группировки, fallback на normalized_name
        product_key = product.canonical_name or product.normalized_name

        if product_key not in grouped:
            grouped[product_key] = {
                "product": product_key,
                "best_price": offer.price,
                "offers_count": 0,
                "offers": []
            }

        grouped[product_key]["offers"].append({
            "source": offer.source,
            "price": offer.price,
            "url": offer.url
        })

        grouped[product_key]["best_price"] = min(
            grouped[product_key]["best_price"],
            offer.price
        )
        grouped[product_key]["offers_count"] += 1

    return {
        "query": q,
        "results": list(grouped.values())
    }

@router.get("/offers")
def all_offers(session: Session = Depends(get_session)):
    return session.exec(select(Offer)).all()
