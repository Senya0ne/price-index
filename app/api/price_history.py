from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.price_history import PriceHistory

router = APIRouter(prefix="/price-history")

@router.get("/")
def history(canonical: str, limit: int = 100, session: Session = Depends(get_session)):
    """Получить историю цен для канонического названия товара (ASC для графика)"""
    try:
        rows = session.exec(
            select(PriceHistory)
            .where(PriceHistory.canonical_name == canonical)
            .order_by(PriceHistory.fetched_at.asc())
            .limit(limit)
        ).all()

        return [
            {
                "price": r.price,
                "source": r.source,
                "at": r.fetched_at.isoformat()
            }
            for r in rows
        ]
    except Exception as e:
        # Возвращаем пустой список при ошибках
        return []
