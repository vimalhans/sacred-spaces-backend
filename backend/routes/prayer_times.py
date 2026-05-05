from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import PlaceOfWorship, PrayerTime
from schemas import PrayerTimeCreate, PrayerTimeResponse

router = APIRouter(prefix="/api/places/{place_id}/prayer-times", tags=["prayer_times"])


@router.post("", response_model=PrayerTimeResponse)
def add_prayer_time(
    place_id: int,
    body: PrayerTimeCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    place = db.query(PlaceOfWorship).filter(PlaceOfWorship.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    if place.created_by != int(user["sub"]):
        raise HTTPException(status_code=403, detail="Not your place of worship")

    pt = PrayerTime(
        place_id=place_id,
        prayer_name=body.prayer_name,
        time=body.time,
        day_of_week=body.day_of_week,
    )
    db.add(pt)
    db.commit()
    db.refresh(pt)
    return pt


@router.delete("/{pt_id}")
def delete_prayer_time(
    place_id: int,
    pt_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    place = db.query(PlaceOfWorship).filter(PlaceOfWorship.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    if place.created_by != int(user["sub"]):
        raise HTTPException(status_code=403, detail="Not your place of worship")

    pt = db.query(PrayerTime).filter(PrayerTime.id == pt_id, PrayerTime.place_id == place_id).first()
    if not pt:
        raise HTTPException(status_code=404, detail="Prayer time not found")
    db.delete(pt)
    db.commit()
    return {"ok": True}
