from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Country
from schemas import CountryResponse

router = APIRouter(prefix="/api/countries", tags=["countries"])


@router.get("", response_model=list[CountryResponse])
def list_countries(db: Session = Depends(get_db)):
    return db.query(Country).order_by(Country.name).all()
