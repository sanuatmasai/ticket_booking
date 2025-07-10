# app/models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Venue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    location: str
    capacity: int

    events: List["Event"] = Relationship(back_populates="venue")

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    date: str
    venue_id: int = Field(foreign_key="venue.id")

    venue: Optional[Venue] = Relationship(back_populates="events")
    bookings: List["Booking"] = Relationship(back_populates="event")

class TicketType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # VIP, Standard, etc.
    price: float

    bookings: List["Booking"] = Relationship(back_populates="ticket_type")

class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    quantity: int
    status: str = "pending"
    # total_price: float

    event_id: int = Field(foreign_key="event.id")
    venue_id: int = Field(foreign_key="venue.id")
    ticket_type_id: int = Field(foreign_key="tickettype.id")

    event: Optional[Event] = Relationship(back_populates="bookings")
    ticket_type: Optional[TicketType] = Relationship(back_populates="bookings")
 