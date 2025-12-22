"""Одноразовый запуск ingestion для тестирования"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlmodel import Session
from app.db.session import engine
from app.sources.avito.service import fetch_and_save_offers

def main():
    print("🟡 Running Avito ingestion once...")
    
    with Session(engine) as session:
        fetch_and_save_offers(session, "xiaomi redmi a27q")
    
    print("🟢 Ingestion completed!")

if __name__ == "__main__":
    main()
