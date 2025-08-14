from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import engine, Base, get_db
from . import schemas, models
from .crud import create_listing, get_listings, get_listing

app = FastAPI(title="Artist Market API")

# Создаём таблицы (в SQLite in-memory это нужно на каждый старт).
Base.metadata.create_all(bind=engine)

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

