from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    place = relationship("PlaceOfWorship", back_populates="owner", uselist=False)


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String(2), unique=True, nullable=False)

    places = relationship("PlaceOfWorship", back_populates="country")


class PlaceOfWorship(Base):
    __tablename__ = "places_of_worship"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    religion = Column(String, nullable=False)
    place_type = Column(String, nullable=False)
    address = Column(String)
    city = Column(String)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    description = Column(Text)
    contact_email = Column(String)
    contact_phone = Column(String)
    website = Column(String)
    image_url = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    is_premium = Column(Boolean, default=False)
    stripe_customer_id = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    country = relationship("Country", back_populates="places")
    owner = relationship("User", back_populates="place")

    @property
    def country_name(self):
        return self.country.name if self.country else ""
    events = relationship("Event", back_populates="place", cascade="all, delete-orphan")
    prayer_times = relationship("PrayerTime", back_populates="place", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    place_id = Column(Integer, ForeignKey("places_of_worship.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    recurring = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    place = relationship("PlaceOfWorship", back_populates="events")


class PrayerTime(Base):
    __tablename__ = "prayer_times"

    id = Column(Integer, primary_key=True, autoincrement=True)
    place_id = Column(Integer, ForeignKey("places_of_worship.id"), nullable=False)
    prayer_name = Column(String, nullable=False)
    time = Column(String, nullable=False)
    day_of_week = Column(String)

    place = relationship("PlaceOfWorship", back_populates="prayer_times")
