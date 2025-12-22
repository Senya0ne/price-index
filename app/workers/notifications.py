"""Worker для проверки падения цен и отправки уведомлений"""
import time
import httpx
import os
from sqlmodel import Session
from app.db.session import engine
from app.models.subscription import Subscription
from sqlmodel import select
from app.core.price_intelligence import check_price_drop

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
API_URL = os.getenv("API_URL", "http://price_api:8000")
BOT_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

INTERVAL = 1800  # 30 минут

def send_notification(user_id: int, canonical: str, drop_percent: float, old_price: float, new_price: float):
    """Отправка уведомления в Telegram"""
    if not BOT_TOKEN:
        print("BOT_TOKEN not set, skipping notification")
        return
    
    message = (
        f"🔻 Цена упала на {drop_percent}%\n\n"
        f"📦 {canonical}\n"
        f"💰 Было: {int(old_price)} ₽\n"
        f"💰 Стало: {int(new_price)} ₽"
    )
    
    try:
        with httpx.Client(timeout=10) as client:
            r = client.post(
                BOT_API_URL,
                json={
                    "chat_id": user_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
            )
            r.raise_for_status()
            print(f"Notification sent to user {user_id}")
    except Exception as e:
        print(f"Error sending notification to user {user_id}: {e}")

def get_price_pair(session: Session, canonical: str):
    """Получить последние 2 цены для сравнения"""
    from sqlalchemy import text
    
    q = text("""
        SELECT price, fetched_at
        FROM pricehistory
        WHERE canonical_name = :canonical
        ORDER BY fetched_at DESC
        LIMIT 2
    """)
    
    rows = list(session.execute(q, {"canonical": canonical}).all())
    
    if len(rows) < 2:
        return None, None
    
    return float(rows[1].price), float(rows[0].price)  # old, new

def check_subscriptions():
    """Проверка всех подписок на падение цен"""
    print("🟡 Checking subscriptions...")
    
    with Session(engine) as session:
        subscriptions = session.exec(select(Subscription)).all()
        
        for sub in subscriptions:
            drop_percent = check_price_drop(session, sub.canonical_name, sub.threshold)
            
            if drop_percent:
                old_price, new_price = get_price_pair(session, sub.canonical_name)
                if old_price and new_price:
                    send_notification(sub.user_id, sub.canonical_name, drop_percent, old_price, new_price)

def run():
    """Бесконечный цикл проверки подписок"""
    while True:
        try:
            check_subscriptions()
        except Exception as e:
            print(f"Error in notifications worker: {e}")
        
        print(f"🟢 Notifications cycle finished, sleeping {INTERVAL}s")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    run()
