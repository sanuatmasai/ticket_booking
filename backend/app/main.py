# app/main.py
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import events, venues, tickets, bookings, analytics

app = FastAPI(title="Ticket Booking System")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Register routers
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(venues.router, prefix="/venues", tags=["Venues"])
app.include_router(tickets.router, prefix="/ticket-types", tags=["Ticket Types"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
app.include_router(analytics.router, tags=["Analytics"])  # No prefix for general queries
