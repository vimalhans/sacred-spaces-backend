from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import create_token, get_current_user, hash_password, verify_password
from database import get_db
from models import PlaceOfWorship, User
from schemas import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=body.email, password_hash=hash_password(body.password))
    db.add(user)
    db.flush()

    place = PlaceOfWorship(
        name=body.place_name,
        religion=body.religion,
        denomination=body.denomination,
        place_type=body.place_type,
        address=body.address,
        city=body.city,
        country_id=body.country_id,
        description=body.description,
        contact_email=body.contact_email,
        contact_phone=body.contact_phone,
        website=body.website,
        image_url=body.image_url,
        latitude=body.latitude,
        longitude=body.longitude,
        created_by=user.id,
    )
    db.add(place)
    db.commit()
    db.refresh(place)

    token = create_token(user.id, place.id)
    return TokenResponse(access_token=token, place_id=place.id, place_name=place.name)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    place = db.query(PlaceOfWorship).filter(PlaceOfWorship.created_by == user.id).first()
    if not place:
        raise HTTPException(status_code=404, detail="No place of worship found for this account")

    token = create_token(user.id, place.id)
    return TokenResponse(access_token=token, place_id=place.id, place_name=place.name)
