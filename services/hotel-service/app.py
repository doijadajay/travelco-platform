from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="TravelCo Hotel Service",
    version="1.0.0",
    description="API for hotel information"
)

hotels = [
    {
        "id": 1,
        "name": "Taj Mumbai",
        "city": "Mumbai",
        "price_per_night": 8500,
        "currency": "INR"
    },
    {
        "id": 2,
        "name": "The Leela Palace",
        "city": "Bengaluru",
        "price_per_night": 12000,
        "currency": "INR"
    },
    {
        "id": 3,
        "name": "Grand Hyatt",
        "city": "Goa",
        "price_per_night": 9500,
        "currency": "INR"
    }
]


@app.get("/health")
def health():
    return {"status": "healthy", "service": "hotel-service"}


@app.get("/hotels")
def get_hotels():
    return {"hotels": hotels}


@app.get("/hotels/{hotel_id}")
def get_hotel(hotel_id: int):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            return hotel

    raise HTTPException(status_code=404, detail="Hotel not found")
