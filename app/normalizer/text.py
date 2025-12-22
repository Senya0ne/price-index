import re

STOPWORDS = [
    "купить", "цена", "дешево", "оригинал"
]

def normalize_title(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^\w\s]", " ", s)

    for w in STOPWORDS:
        s = s.replace(w, "")

    s = re.sub(r"\s+", " ", s).strip()
    return s
