from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="TravelCo Payment Service",
    version="1.0.0",
    description="API for payment processing"
)

payments = {}


class PaymentRequest(BaseModel):
    booking_id: str = Field(min_length=1)
    amount: float = Field(gt=0)
    currency: str = "INR"


@app.get("/health")
def health():
    return {"status": "healthy", "service": "payment-service"}


@app.post("/payments", status_code=201)
def create_payment(request: PaymentRequest):
    payment_id = str(uuid4())

    payment = {
        "payment_id": payment_id,
        "booking_id": request.booking_id,
        "amount": request.amount,
        "currency": request.currency,
        "status": "SUCCESS",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    payments[payment_id] = payment
    return payment


@app.get("/payments")
def get_payments():
    return {"payments": list(payments.values())}


@app.get("/payments/{payment_id}")
def get_payment(payment_id: str):
    payment = payments.get(payment_id)

    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment
