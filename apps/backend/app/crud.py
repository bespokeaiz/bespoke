from sqlalchemy.orm import Session
from . import models, schemas

def create_listing(db: Session, data: schemas.ListingIn) -> models.Listing:
    item = models.Listing(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_listings(db: Session) -> list[models.Listing]:
    return list(db.query(models.Listing).order_by(models.Listing.id.desc()))
    
def get_listing(db: Session, listing_id: int) -> models.Listing | None:
    return db.query(models.Listing).filter(models.Listing.id == listing_id).first()
