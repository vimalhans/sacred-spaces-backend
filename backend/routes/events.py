from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Event, PlaceOfWorship
from schemas import EventCreate, EventResponse

router = APIRouter(prefix="/api/places/{place_id}/events", tags=["events"])


@router.post("", response_model=EventResponse)
def add_event(
    place_id: int,
    body: EventCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    place = db.query(PlaceOfWorship).filter(PlaceOfWorship.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    if place.created_by != int(user["sub"]):
        raise HTTPException(status_code=403, detail="Not your place of worship")

    event = Event(
        place_id=place_id,
        title=body.title,
        description=body.description or "",
        start_time=datetime.fromisoformat(body.start_time),
        end_time=datetime.fromisoformat(body.end_time) if body.end_time else None,
        recurring=body.recurring,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.delete("/{event_id}")
def delete_event(
    place_id: int,
    event_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    place = db.query(PlaceOfWorship).filter(PlaceOfWorship.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    if place.created_by != int(user["sub"]):
        raise HTTPException(status_code=403, detail="Not your place of worship")

    event = db.query(Event).filter(Event.id == event_id, Event.place_id == place_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return {"ok": True}
