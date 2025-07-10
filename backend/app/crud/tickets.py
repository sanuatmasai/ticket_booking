# app/crud/tickets.py
from sqlalchemy.orm import Session
from app import models

def create_ticket_type(db: Session, ticket_type: models.TicketType):
    db.add(ticket_type)
    db.commit()
    db.refresh(ticket_type)
    return ticket_type

def get_all_ticket_types(db: Session):
    return db.query(models.TicketType).all()

def get_bookings_by_ticket_type(db: Session, ticket_type_id: int):
    return db.query(models.Booking).filter(models.Booking.ticket_type_id == ticket_type_id).all()
 