# app/routers/venues.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_session
from app.crud import venues as venue_crud

router = APIRouter()

@router.post("/", response_model=schemas.VenueRead)
def create_venue(venue: schemas.VenueCreate, db: Session = Depends(get_session)):
    venue_obj = models.Venue(**venue.dict())
    return venue_crud.create_venue(db, venue_obj)

@router.get("/", response_model=list[schemas.VenueRead])
def get_all_venues(db: Session = Depends(get_session)):
    return venue_crud.get_all_venues(db)

@router.get("/{venue_id}/events", response_model=list[schemas.EventRead])
def get_events_for_venue(venue_id: int, db: Session = Depends(get_session)):
    events = venue_crud.get_events_by_venue(db, venue_id)
    if not events:
        raise HTTPException(status_code=404, detail="No events found for this venue")
    return events
 