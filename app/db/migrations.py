"""Скрипт для создания индексов и миграций"""
from sqlalchemy import text
from app.db.session import engine

def create_indexes():
    """Создание дополнительных индексов для оптимизации"""
    with engine.connect() as conn:
        # Составной индекс для быстрого поиска истории цен
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_pricehistory_canonical_time
            ON pricehistory (canonical_name, fetched_at DESC)
        """))
        conn.commit()
