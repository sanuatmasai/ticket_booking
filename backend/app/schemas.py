# app/schemas.py
from typing import Optional
from pydantic import BaseModel

class VenueCreate(BaseModel):
    name: str
    location: str
    capacity: int

class VenueRead(VenueCreate):
    id: int

class EventCreate(BaseModel):
    name: str
    date: str
    venue_id: int

class EventRead(EventCreate):
    id: int

# class BookingRead(BaseModel):
#     id: int
#     user_name: str
#     quantity: int
#     status: str
#     ticket_type_id: int

class TicketTypeCreate(BaseModel):
    name: str
    price: float

class TicketTypeRead(TicketTypeCreate):
    id: int

class BookingCreate(BaseModel):
    user_name: str
    event_id: int
    ticket_type_id: int
    quantity: int

class BookingUpdate(BaseModel):
    user_name: Optional[str] = None
    ticket_type_id: Optional[int] = None
    quantity: Optional[int] = None

class BookingStatusUpdate(BaseModel):
    status: str  # confirmed, cancelled, pending

class BookingRead(BaseModel):
    id: int
    user_name: str
    event_id: int
    ticket_type_id: int
    quantity: int
    status: str
    # total_price: float

    class Config:
        orm_mode = True
