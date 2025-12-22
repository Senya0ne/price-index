from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Offer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", index=True)

    source: str  # e.g., ozon, wb, market, avito
    price: float
    url: str

    delivery: Optional[str]
    availability: Optional[bool]

    fetched_at: datetime = Field(default_factory=datetime.utcnow)
