from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.sources.ozon.service import fetch_and_save_offers
from app.sources.wb.service import fetch_and_save_offers as wb_ingest
from app.sources.avito.service import fetch_and_save_offers as ingest_avito

router = APIRouter(prefix="/ingest")

@router.post("/ozon")
def ingest_ozon(q: str, session: Session = Depends(get_session)):
    fetch_and_save_offers(session, q)
    print("INGEST OZON", q)
    return {"status": "ok", "source": "ozon"}

@router.post("/wb")
def ingest_wb(q: str, session: Session = Depends(get_session)):
    wb_ingest(session, q)
    return {"status": "ok", "source": "wildberries"}

@router.post("/avito")
def ingest_avito_endpoint(q: str, session: Session = Depends(get_session)):
    ingest_avito(session, q)
    return {"status": "ok", "source": "avito"}

