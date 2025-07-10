# app/crud/events.py
from sqlalchemy.orm import Session
from app import models

def create_event(db: Session, event: models.Event):
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_all_events(db: Session):
    return db.query(models.Event).all()

def get_bookings_for_event(db: Session, event_id: int):
    return db.query(models.Booking).filter(models.Booking.event_id == event_id).all()

def get_available_tickets(db: Session, event_id: int):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    venue = db.query(models.Venue).filter(models.Venue.id == event.venue_id).first()

    total_capacity = venue.capacity
    booked_tickets = db.query(models.Booking).filter(
        models.Booking.event_id == event_id,
        models.Booking.status == "confirmed"
    ).with_entities(models.Booking.quantity)

    total_booked = sum(b.quantity for b in booked_tickets)

    return total_capacity - total_booked
 