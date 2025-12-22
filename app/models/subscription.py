"""Модель подписки пользователя на уведомления о ценах"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # Telegram user_id
    canonical_name: str = Field(index=True)
    threshold: float = Field(default=10.0)  # Процент падения для уведомления
    created_at: datetime = Field(default_factory=datetime.utcnow)
