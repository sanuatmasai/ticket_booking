# app/crud/bookings.py
from sqlalchemy.orm import Session
from app import models
from fastapi import HTTPException

def calculate_total_price(db: Session, ticket_type_id: int, quantity: int) -> float:
    ticket_type = db.query(models.TicketType).filter(models.TicketType.id == ticket_type_id).first()
    if not ticket_type:
        raise HTTPException(status_code=404, detail="Ticket type not found")
    return ticket_type.price * quantity

def get_confirmed_quantity(db: Session, event_id: int) -> int:
    bookings = db.query(models.Booking).filter(
        models.Booking.event_id == event_id,
        models.Booking.status == "confirmed"
    ).all()
    return sum(b.quantity for b in bookings)

def create_booking(db: Session, booking_data):
    event = db.query(models.Event).filter(models.Event.id == booking_data.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    venue = db.query(models.Venue).filter(models.Venue.id == event.venue_id).first()
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")

    confirmed_quantity = get_confirmed_quantity(db, booking_data.event_id)
    if confirmed_quantity + booking_data.quantity > venue.capacity:
        raise HTTPException(status_code=400, detail="Venue capacity exceeded")

    total_price = calculate_total_price(db, booking_data.ticket_type_id, booking_data.quantity)

    booking = models.Booking(
        user_name=booking_data.user_name,
        event_id=booking_data.event_id,
        venue_id=event.venue_id,
        ticket_type_id=booking_data.ticket_type_id,
        quantity=booking_data.quantity,
        status="pending",
        # total_price=total_price
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def get_all_bookings(db: Session):
    return db.query(models.Booking).all()

def update_booking(db: Session, booking_id: int, data):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(booking, key, value)

    # Recalculate price if ticket_type or quantity changed
    # if data.ticket_type_id or data.quantity:
    #     ticket_type_id = data.ticket_type_id or booking.ticket_type_id
    #     quantity = data.quantity or booking.quantity
        # booking.total_price = calculate_total_price(db, ticket_type_id, quantity)

    db.commit()
    db.refresh(booking)
    return booking

def update_booking_status(db: Session, booking_id: int, new_status: str):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = new_status
    db.commit()
    db.refresh(booking)
    return booking

def delete_booking(db: Session, booking_id: int):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
 