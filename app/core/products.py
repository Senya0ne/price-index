import re
from sqlmodel import Session, select
from app.models.product import Product

def normalize_text(text: str) -> str:
    """Нормализация текста: нижний регистр, только буквы/цифры/пробелы"""
    text = text.lower()
    text = re.sub(r"[^a-z0-9а-яё\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def make_canonical_name(brand: str | None, model: str | None) -> str:
    """Создание canonical_name из бренда и модели"""
    parts = []
    if brand:
        parts.append(brand.lower().strip())
    if model:
        parts.append(model.lower().strip())
    return " ".join(parts)

def get_or_create_product(
    session: Session,
    normalized_name: str,
    canonical_name: str,
    brand: str | None = None,
    model: str | None = None
) -> Product:
    """Получить или создать продукт. Ищем по canonical_name для дедупликации."""
    # Сначала ищем по canonical_name для дедупликации
    product = session.exec(
        select(Product).where(Product.canonical_name == canonical_name)
    ).first()

    if product:
        # Обновляем normalized_name если отличается
        if product.normalized_name != normalized_name:
            product.normalized_name = normalized_name
            if brand:
                product.brand = brand
            if model:
                product.model = model
            session.add(product)
            session.commit()
            session.refresh(product)
        return product

    # Создаём новый продукт
    product = Product(
        normalized_name=normalized_name,
        canonical_name=canonical_name,
        brand=brand,
        model=model
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
