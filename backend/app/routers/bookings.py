 # app/routers/bookings.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_session
from app.crud import bookings as crud

router = APIRouter()

@router.post("/", response_model=schemas.BookingRead)
def create_booking(data: schemas.BookingCreate, db: Session = Depends(get_session)):
    return crud.create_booking(db, data)

@router.get("/", response_model=list[schemas.BookingRead])
def get_all_bookings(db: Session = Depends(get_session)):
    return crud.get_all_bookings(db)

@router.put("/{booking_id}", response_model=schemas.BookingRead)
def update_booking(booking_id: int, data: schemas.BookingUpdate, db: Session = Depends(get_session)):
    return crud.update_booking(db, booking_id, data)

@router.patch("/{booking_id}/status", response_model=schemas.BookingRead)
def update_status(booking_id: int, data: schemas.BookingStatusUpdate, db: Session = Depends(get_session)):
    return crud.update_booking_status(db, booking_id, data.status)

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_session)):
    crud.delete_booking(db, booking_id)
    return {"detail": "Booking deleted"}
