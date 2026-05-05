import os
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
from database import get_db
from models import PlaceOfWorship, User
from auth import get_current_user

# Stripe Keys (should be in .env)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_mock")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

router = APIRouter(prefix="/api/stripe", tags=["stripe"])

@router.post("/create-checkout-session")
async def create_checkout_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    place = db.query(PlaceOfWorship).filter(PlaceOfWorship.created_by == current_user.id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    try:
        # Create or retrieve customer
        if not place.stripe_customer_id:
            customer = stripe.Customer.create(
                email=current_user.email,
                name=place.name,
                metadata={"place_id": place.id}
            )
            place.stripe_customer_id = customer.id
            db.commit()
        
        # Create Checkout Session
        # Replace 'price_mock' with your actual Stripe Price ID
        session = stripe.checkout.Session.create(
            customer=place.stripe_customer_id,
            payment_method_types=['card'],
            line_items=[
                {
                    'price': os.getenv("STRIPE_PRICE_ID", "price_mock"),
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=f"{FRONTEND_URL}/dashboard?status=success",
            cancel_url=f"{FRONTEND_URL}/dashboard?status=cancel",
            metadata={"place_id": place.id}
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    db: Session = Depends(get_db)
):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid payload or signature")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        place_id = session.get('metadata', {}).get('place_id')
        if place_id:
            place = db.query(PlaceOfWorship).filter(PlaceOfWorship.id == int(place_id)).first()
            if place:
                place.is_premium = True
                db.commit()

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        customer_id = subscription.get('customer')
        if customer_id:
            place = db.query(PlaceOfWorship).filter(PlaceOfWorship.stripe_customer_id == customer_id).first()
            if place:
                place.is_premium = False
                db.commit()

    return {"status": "success"}
