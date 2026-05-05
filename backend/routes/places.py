from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Country, Event, PlaceOfWorship, PrayerTime
from schemas import PlaceResponse, PlaceUpdate

router = APIRouter(prefix="/api/places", tags=["places"])


@router.get("", response_model=list[PlaceResponse])
def list_places(
    country_id: int | None = Query(None),
    religion: str | None = Query(None),
    place_type: str | None = Query(None),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(PlaceOfWorship)
    if country_id:
        q = q.filter(PlaceOfWorship.country_id == country_id)
    if religion:
        q = q.filter(PlaceOfWorship.religion.ilike(f"%{religion}%"))
    if place_type:
        q = q.filter(PlaceOfWorship.place_type.ilike(f"%{place_type}%"))
    if search:
        q = q.filter(
            PlaceOfWorship.name.ilike(f"%{search}%")
            | PlaceOfWorship.city.ilike(f"%{search}%")
            | PlaceOfWorship.description.ilike(f"%{search}%")
        )
    return q.all()


@router.get("/{place_id}", response_model=PlaceResponse)
def get_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(PlaceOfWorship).filter(PlaceOfWorship.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.put("/{place_id}", response_model=PlaceResponse)
def update_place(
    place_id: int,
    body: PlaceUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    place = db.query(PlaceOfWorship).filter(PlaceOfWorship.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    if place.created_by != int(user["sub"]):
        raise HTTPException(status_code=403, detail="Not your place of worship")

    for attr, value in body.model_dump(exclude_unset=True).items():
        setattr(place, attr, value)
    db.commit()
    db.refresh(place)
    return place


@router.get("/me/managed", response_model=PlaceResponse)
def get_my_place(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    place = (
        db.query(PlaceOfWorship)
        .filter(PlaceOfWorship.created_by == int(user["sub"]))
        .first()
    )
    if not place:
        raise HTTPException(status_code=404, detail="No place found")
    return place
