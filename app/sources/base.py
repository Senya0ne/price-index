"""Базовые утилиты для источников данных"""
from sqlmodel import Session
from app.models.price_history import PriceHistory

def save_price_history(session: Session, canonical_name: str, source: str, price: float):
    """Сохранить снапшот цены в историю. Всегда пишем, не проверяем изменения."""
    session.add(
        PriceHistory(
            canonical_name=canonical_name,
            source=source,
            price=price
        )
    )
