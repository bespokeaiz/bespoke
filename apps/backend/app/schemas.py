from pydantic import BaseModel, Field

class ListingIn(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=3, max_length=2000)
    price_from: float = Field(..., ge=0)
    city: str
    category: str

class Listing(ListingIn):
    id: int
