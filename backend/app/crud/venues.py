# app/crud/venues.py
from sqlalchemy.orm import Session
from app import models

def create_venue(db: Session, venue: models.Venue):
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue

def get_all_venues(db: Session):
    return db.query(models.Venue).all()

def get_events_by_venue(db: Session, venue_id: int):
    return db.query(models.Event).filter(models.Event.venue_id == venue_id).all()
 