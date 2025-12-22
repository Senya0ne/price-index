"""Функции для анализа цен"""
from sqlalchemy import text
from sqlmodel import Session

def check_price_drop(session: Session, canonical: str, threshold: float = 10.0) -> float | None:
    """
    Проверяет падение цены на основе последних 2 записей.
    Возвращает процент падения, если падение >= threshold, иначе None.
    """
    q = text("""
        SELECT price
        FROM pricehistory
        WHERE canonical_name = :canonical
        ORDER BY fetched_at DESC
        LIMIT 2
    """)

    rows = list(session.execute(q, {"canonical": canonical}).all())

    if len(rows) < 2:
        return None

    # rows[0] - последняя (новая) цена, rows[1] - предыдущая (старая) цена
    new_price = float(rows[0].price)
    old_price = float(rows[1].price)

    if old_price == 0:
        return None

    drop_percent = ((old_price - new_price) / old_price) * 100

    if drop_percent >= threshold:
        return round(drop_percent, 1)

    return None
