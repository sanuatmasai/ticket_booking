# We'll now implement advanced query endpoints:
# - /bookings/search
# - /booking-system/stats
# - /events/{id}/revenue
# - /venues/{id}/occupancy

# app/routers/analytics.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_session
from app import models

router = APIRouter()

@router.get("/bookings/search")
def search_bookings(
    event: str = Query(None),
    venue: str = Query(None),
    ticket_type: str = Query(None),
    db: Session = Depends(get_session)
):
    query = db.query(models.Booking, models.Event, models.Venue, models.TicketType).\
        join(models.Event).\
        join(models.Venue, models.Event.venue_id == models.Venue.id).\
        join(models.TicketType, models.Booking.ticket_type_id == models.TicketType.id)

    if event:
        query = query.filter(models.Event.name.ilike(f"%{event}%"))
    if venue:
        query = query.filter(models.Venue.name.ilike(f"%{venue}%"))
    if ticket_type:
        query = query.filter(models.TicketType.name.ilike(f"%{ticket_type}%"))

    results = query.all()
    return [
        {
            "booking_id": b.Booking.id,
            "user": b.Booking.user_name,
            "event": b.Event.name,
            "venue": b.Venue.name,
            "ticket_type": b.TicketType.name,
            "quantity": b.Booking.quantity,
            "status": b.Booking.status
        } for b in results
    ]

@router.get("/booking-system/stats")
def booking_stats(db: Session = Depends(get_session)):
    total_bookings = db.query(models.Booking).count()
    total_events = db.query(models.Event).count()
    total_venues = db.query(models.Venue).count()
    total_tickets_available = 0

    events = db.query(models.Event).all()
    for event in events:
        venue = db.query(models.Venue).filter(models.Venue.id == event.venue_id).first()
        confirmed = db.query(models.Booking).filter(
            models.Booking.event_id == event.id,
            models.Booking.status == "confirmed"
        ).all()
        booked = sum(b.quantity for b in confirmed)
        total_tickets_available += (venue.capacity - booked)

    return {
        "total_bookings": total_bookings,
        "total_events": total_events,
        "total_venues": total_venues,
        "total_available_tickets": total_tickets_available
    }

@router.get("/events/{event_id}/revenue")
def event_revenue(event_id: int, db: Session = Depends(get_session)):
    total = db.query(func.sum(models.Booking.total_price)).filter(
        models.Booking.event_id == event_id,
        models.Booking.status == "confirmed"
    ).scalar() or 0.0
    return {"event_id": event_id, "revenue": total}

@router.get("/venues/{venue_id}/occupancy")
def venue_occupancy(venue_id: int, db: Session = Depends(get_session)):
    venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if not venue:
        return {"error": "Venue not found"}

    events = db.query(models.Event).filter(models.Event.venue_id == venue_id).all()
    total_capacity = venue.capacity * len(events)
    confirmed = db.query(models.Booking).join(models.Event).filter(
        models.Event.venue_id == venue_id,
        models.Booking.status == "confirmed"
    ).all()
    total_booked = sum(b.quantity for b in confirmed)
    return {
        "venue_id": venue_id,
        "capacity": total_capacity,
        "booked": total_booked,
        "occupancy_percent": round((total_booked / total_capacity) * 100, 2) if total_capacity else 0
    }
