from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import get_db
from . import schemas
from .crud import create_listing, get_listings, get_listing

from sqlalchemy.exc import OperationalError
import time

app = FastAPI(title="Artist Market API")

def wait_for_db(max_retries: int = 30, delay: float = 1.0):
    """Ждём, пока Postgres примет коннект."""
    from .db import engine  # локальный импорт, чтобы не цеплять раньше времени
    for _ in range(max_retries):
        try:
            with engine.connect() as _:
                return
        except OperationalError:
            time.sleep(delay)
    raise RuntimeError("Database is not ready after waiting")

@app.on_event("startup")
def on_startup():
    # ждём готовности БД; таблицы создаёт Alembic, поэтому create_all не вызываем
    wait_for_db()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/listings", response_model=list[schemas.Listing])
def list_listings(db: Session = Depends(get_db)):
    return get_listings(db)

@app.post("/listings", response_model=schemas.Listing, status_code=201)
def post_listing(payload: schemas.ListingIn, db: Session = Depends(get_db)):
    return create_listing(db, payload)

@app.get("/listings/{listing_id}", response_model=schemas.Listing)
def read_listing(listing_id: int, db: Session = Depends(get_db)):
    item = get_listing(db, listing_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item
