from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.price_history import PriceHistory

router = APIRouter(prefix="/history")

@router.get("/{offer_id}")
def history(offer_id: int, session: Session = Depends(get_session)):
    """Получить историю цен для конкретного оффера"""
    return session.exec(
        select(PriceHistory)
        .where(PriceHistory.offer_id == offer_id)
        .order_by(PriceHistory.fetched_at.desc())
        .limit(100)
    ).all()
