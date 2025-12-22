from sqlmodel import SQLModel, Field
from typing import Optional

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    normalized_name: str = Field(index=True)
    canonical_name: Optional[str] = Field(default=None, index=True)  # Для дедупликации
    brand: Optional[str]
    model: Optional[str]
