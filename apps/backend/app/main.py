from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="Artist Market API")

# Простая "память" процесса. На проде тут будет БД.
DB: List[dict] = []
ID = 1

class ListingIn(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=3, max_length=1000)
    price_from: float = Field(..., ge=0)
    city: str
    category: str

class Listing(ListingIn):
    id: int

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/listings", response_model=List[Listing])
def list_listings():
    return DB

@app.post("/listings", response_model=Listing, status_code=201)
def create_listing(payload: ListingIn):
    global ID
    item = {"id": ID, **payload.model_dump()}
    DB.append(item)
    ID += 1
    return item

@app.get("/listings/{listing_id}", response_model=Listing)
def get_listing(listing_id: int):
    for item in DB:
        if item["id"] == listing_id:
            return item
    raise HTTPException(status_code=404, detail="Not found")
