# app/routers/tickets.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_session
from app.crud import tickets as ticket_crud

router = APIRouter()

@router.post("/", response_model=schemas.TicketTypeRead)
def create_ticket_type(ticket_type: schemas.TicketTypeCreate, db: Session = Depends(get_session)):
    ticket = models.TicketType(**ticket_type.dict())
    return ticket_crud.create_ticket_type(db, ticket)

@router.get("/", response_model=list[schemas.TicketTypeRead])
def get_all_ticket_types(db: Session = Depends(get_session)):
    return ticket_crud.get_all_ticket_types(db)

@router.get("/{type_id}/bookings", response_model=list[schemas.BookingRead])
def get_bookings_for_ticket_type(type_id: int, db: Session = Depends(get_session)):
    bookings = ticket_crud.get_bookings_by_ticket_type(db, type_id)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this ticket type")
    return bookings
 