from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Auth
class RegisterRequest(BaseModel):
    email: str
    password: str
    place_name: str
    religion: str
    denomination: str = ""
    place_type: str
    address: str = ""
    city: str = ""
    country_id: int
    description: str = ""
    contact_email: str = ""
    contact_phone: str = ""
    website: str = ""
    image_url: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    place_id: int
    place_name: str


# Countries
class CountryResponse(BaseModel):
    id: int
    name: str
    code: str

    model_config = {"from_attributes": True}


# Prayer Times
class PrayerTimeResponse(BaseModel):
    id: int
    prayer_name: str
    time: str
    day_of_week: Optional[str] = None

    model_config = {"from_attributes": True}


class PrayerTimeCreate(BaseModel):
    prayer_name: str
    time: str
    day_of_week: Optional[str] = None


# Events
class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    recurring: bool = False

    model_config = {"from_attributes": True}


class EventCreate(BaseModel):
    title: str
    description: str = ""
    start_time: str
    end_time: str = ""
    recurring: bool = False


# Places
class PlaceResponse(BaseModel):
    id: int
    name: str
    religion: str
    denomination: Optional[str] = None
    place_type: str
    address: Optional[str] = None
    city: Optional[str] = None
    country_id: int
    country_name: str = ""
    description: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_premium: bool = False
    events: list[EventResponse] = []
    prayer_times: list[PrayerTimeResponse] = []

    model_config = {"from_attributes": True}


class PlaceUpdate(BaseModel):
    name: Optional[str] = None
    religion: Optional[str] = None
    denomination: Optional[str] = None
    place_type: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    description: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
