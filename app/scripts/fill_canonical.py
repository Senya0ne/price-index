import sys
import os

# Добавляем корневую директорию в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlmodel import Session, select
from app.db.session import engine
from app.models.product import Product
from app.core.products import normalize_text

RULES = [
    ("xiaomi redmi a27q", ["a27q"]),
]

def detect_canonical(normalized: str) -> str | None:
    """Определяет canonical_name на основе правил"""
    for canonical, keys in RULES:
        if all(k in normalized for k in keys):
            return canonical
    return None


def main():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()

        updated = 0
        for p in products:
            if p.canonical_name:
                continue

            normalized = normalize_text(p.normalized_name)
            canonical = detect_canonical(normalized)

            if canonical:
                p.canonical_name = canonical
                session.add(p)
                updated += 1

        session.commit()
        print(f"Updated {updated} products")


if __name__ == "__main__":
    main()
