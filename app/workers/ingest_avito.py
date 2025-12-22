import time
from sqlmodel import Session
from app.db.session import engine
from app.sources.avito.service import fetch_and_save_offers

QUERIES = [
    "xiaomi redmi a27q",
    # потом добавим динамически
]

INTERVAL = 1800  # 30 минут

def run():
    while True:
        print("🟡 Avito ingestion cycle started")

        with Session(engine) as session:
            for q in QUERIES:
                fetch_and_save_offers(session, q)

        print("🟢 Avito ingestion cycle finished")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    run()
