import re

STOP_WORDS = [
    "монитор", "дисплей", "ips", "2k", "27", "дюйм", "гц",
    "новинка", "2024", "2025"
]

def normalize_product_name(name: str) -> str:
    """Нормализация названия товара для получения canonical_name"""
    name = name.lower()

    for w in STOP_WORDS:
        name = name.replace(w, "")

    name = re.sub(r"[^a-z0-9 ]", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()
