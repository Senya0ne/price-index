from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlmodel import Session
from app.db.session import get_session

router = APIRouter()

@router.get("/price-stats/")
def stats(canonical: str, days: int = 30, session: Session = Depends(get_session)):
    """Статистика цен: min, avg, max за период"""
    q = text("""
        SELECT
          MIN(price)  AS min_price,
          AVG(price)  AS avg_price,
          MAX(price)  AS max_price
        FROM pricehistory
        WHERE canonical_name = :canonical
          AND fetched_at >= NOW() - (:days || ' days')::interval
    """)

    result = session.execute(q, {"canonical": canonical, "days": days}).first()

    if not result or result.min_price is None:
        return {
            "canonical": canonical,
            "days": days,
            "min": None,
            "avg": None,
            "max": None,
        }

    return {
        "canonical": canonical,
        "days": days,
        "min": float(result.min_price),
        "avg": float(result.avg_price),
        "max": float(result.max_price),
    }

@router.get("/best-price/")
def best_price(canonical: str, session: Session = Depends(get_session)):
    """Текущая лучшая (минимальная) цена с fallback"""
    q = text("""
        SELECT source, price, fetched_at
        FROM pricehistory
        WHERE canonical_name = :canonical
        ORDER BY price ASC, fetched_at DESC
        LIMIT 1
    """)

    result = session.execute(q, {"canonical": canonical}).first()

    if not result:
        # Fallback: если нет истории, ищем в текущих офферах
        from sqlmodel import select
        from app.models.product import Product
        from app.models.offer import Offer
        
        product = session.exec(
            select(Product).where(Product.canonical_name == canonical)
        ).first()
        
        if product:
            best_offer = session.exec(
                select(Offer)
                .where(Offer.product_id == product.id)
                .order_by(Offer.price.asc())
                .limit(1)
            ).first()
            
            if best_offer:
                return {
                    "canonical": canonical,
                    "price": float(best_offer.price),
                    "source": best_offer.source,
                    "at": best_offer.fetched_at.isoformat() if hasattr(best_offer.fetched_at, 'isoformat') else str(best_offer.fetched_at)
                }
        
        return {"canonical": canonical, "price": None, "source": None, "at": None}

    return {
        "canonical": canonical,
        "price": float(result.price),
        "source": result.source,
        "at": result.fetched_at.isoformat() if hasattr(result.fetched_at, 'isoformat') else str(result.fetched_at)
    }
