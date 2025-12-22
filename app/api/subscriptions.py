"""API для управления подписками на уведомления о ценах"""
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.subscription import Subscription

router = APIRouter(prefix="/subscriptions")

@router.post("/")
def create_subscription(user_id: int, canonical: str, threshold: float = 10.0, session: Session = Depends(get_session)):
    """Создать подписку на уведомления о падении цены"""
    # Проверяем, есть ли уже подписка
    existing = session.exec(
        select(Subscription).where(
            Subscription.user_id == user_id,
            Subscription.canonical_name == canonical
        )
    ).first()
    
    if existing:
        existing.threshold = threshold
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing
    
    subscription = Subscription(
        user_id=user_id,
        canonical_name=canonical,
        threshold=threshold
    )
    session.add(subscription)
    session.commit()
    session.refresh(subscription)
    return subscription

@router.delete("/{user_id}")
def delete_subscription(user_id: int, canonical: str, session: Session = Depends(get_session)):
    """Удалить подписку (canonical передаётся как query параметр)"""
    subscription = session.exec(
        select(Subscription).where(
            Subscription.user_id == user_id,
            Subscription.canonical_name == canonical
        )
    ).first()
    
    if subscription:
        session.delete(subscription)
        session.commit()
        return {"status": "deleted"}
    
    return {"status": "not_found"}

@router.get("/{user_id}")
def list_subscriptions(user_id: int, session: Session = Depends(get_session)):
    """Список подписок пользователя"""
    subscriptions = session.exec(
        select(Subscription).where(Subscription.user_id == user_id)
    ).all()
    
    return subscriptions

@router.get("/")
def all_subscriptions(session: Session = Depends(get_session)):
    """Все подписки (для worker'а)"""
    subscriptions = session.exec(select(Subscription)).all()
    return subscriptions
