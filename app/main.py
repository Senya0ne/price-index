from fastapi import FastAPI
from app.db.init import create_db_and_tables
from app.api import search, ingest, history, price_history, price_stats, subscriptions

app = FastAPI(
    title="Price Aggregator MVP",
    version="0.1.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(search.router)
app.include_router(ingest.router)
app.include_router(history.router)
app.include_router(price_history.router)
app.include_router(price_stats.router)
app.include_router(subscriptions.router)
