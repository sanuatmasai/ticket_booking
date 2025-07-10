 # app/routers/events.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_session
from app.crud import events as event_crud

router = APIRouter()

@router.post("/", response_model=schemas.EventRead)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_session)):
    event_obj = models.Event(**event.dict())
    return event_crud.create_event(db, event_obj)

@router.get("/", response_model=list[schemas.EventRead])
def get_all_events(db: Session = Depends(get_session)):
    return event_crud.get_all_events(db)

@router.get("/{event_id}/bookings", response_model=list[schemas.BookingRead])
def get_event_bookings(event_id: int, db: Session = Depends(get_session)):
    return event_crud.get_bookings_for_event(db, event_id)

@router.get("/{event_id}/available-tickets")
def get_available_tickets(event_id: int, db: Session = Depends(get_session)):
    available = event_crud.get_available_tickets(db, event_id)
    return {"available_tickets": available}
