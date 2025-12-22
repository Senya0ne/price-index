from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class PriceHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    canonical_name: str = Field(index=True)
    source: str = Field(index=True)
    price: float
    fetched_at: datetime = Field(default_factory=datetime.utcnow, index=True)
