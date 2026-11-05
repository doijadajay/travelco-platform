from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="TravelCo Booking Service",
    version="1.0.0",
    description="API for hotel bookings"
)

bookings = {}


class BookingRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    hotel_id: int = Field(gt=0)
    nights: int = Field(gt=0, le=30)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "booking-service"}


@app.post("/bookings", status_code=201)
def create_booking(request: BookingRequest):
    booking_id = str(uuid4())

    booking = {
        "booking_id": booking_id,
        "customer_name": request.customer_name,
        "hotel_id": request.hotel_id,
        "nights": request.nights,
        "status": "CONFIRMED",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    bookings[booking_id] = booking
    return booking


@app.get("/bookings")
def get_bookings():
    return {"bookings": list(bookings.values())}


@app.get("/bookings/{booking_id}")
def get_booking(booking_id: str):
    booking = bookings.get(booking_id)

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking
