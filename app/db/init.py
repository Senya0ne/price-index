from sqlmodel import SQLModel
from app.db.session import engine
from app.models.product import Product
from app.models.offer import Offer
from app.models.price_history import PriceHistory
from app.models.subscription import Subscription
from app.db.migrations import create_indexes

def create_db_and_tables():
    """Создание таблиц и индексов"""
    SQLModel.metadata.create_all(engine)
    create_indexes()
