from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from models import Base, Country, Event, PlaceOfWorship, PrayerTime, User
from auth import hash_password

DATABASE_URL = "sqlite:///worship.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def seed():
    db = Session(engine)
    try:
        Base.metadata.create_all(bind=engine)

        # Simple migration: add denomination column if it doesn't exist
        try:
            db.execute(text("ALTER TABLE places_of_worship ADD COLUMN denomination TEXT"))
            db.commit()
        except Exception:
            pass # Already exists or table not created yet

        if db.query(Country).count() > 30:
            return

        countries = [
            ("US", "United States"), ("GB", "United Kingdom"), ("SA", "Saudi Arabia"),
            ("IN", "India"), ("IL", "Israel"), ("IT", "Italy"), ("FR", "France"),
            ("EG", "Egypt"), ("TR", "Turkey"), ("NG", "Nigeria"), ("BR", "Brazil"),
            ("ID", "Indonesia"), ("PK", "Pakistan"), ("JP", "Japan"), ("KR", "South Korea"),
            ("DE", "Germany"), ("ES", "Spain"), ("TH", "Thailand"), ("RU", "Russia"),
            ("CA", "Canada"), ("AU", "Australia"), ("IE", "Ireland"), ("NL", "Netherlands"),
            ("ZA", "South Africa"), ("KE", "Kenya"), ("AE", "United Arab Emirates"),
            ("MX", "Mexico"), ("MU", "Mauritius"), ("FI", "Finland"), ("SE", "Sweden"),
            ("NO", "Norway"), ("DK", "Denmark"), ("GR", "Greece"), ("CH", "Switzerland"),
            ("BE", "Belgium"), ("PT", "Portugal"), ("MY", "Malaysia"), ("SG", "Singapore"),
        ]
        for code, name in countries:
            if not db.query(Country).filter(Country.code == code).first():
                db.add(Country(code=code, name=name))
        db.flush()

        # Create a demo user with a placeholder place first
        if not db.query(User).filter(User.email == "demo@worshipapp.com").first():
            demo_user = User(email="demo@worshipapp.com", password_hash=hash_password("demo123"))
            db.add(demo_user)
            db.flush()

        places_data = [
            {
                "name": "St. Peter's Basilica",
                "religion": "Christianity", "place_type": "Church",
                "address": "Piazza San Pietro", "city": "Vatican City",
                "country_id": 1,
                "description": "One of the largest churches in the world and the center of the Catholic faith.",
                "image_url": "https://images.unsplash.com/photo-1555991780-4c6a1ef2a7a7?w=600",
                "latitude": 41.9022, "longitude": 12.4539,
            },
            {
                "name": "Masjid al-Haram",
                "religion": "Islam", "place_type": "Mosque",
                "address": "Al Haram", "city": "Mecca",
                "country_id": 3,
                "description": "The holiest mosque in Islam, surrounding the Kaaba.",
                "image_url": "https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?w=600",
                "latitude": 21.4225, "longitude": 39.8262,
            },
            {
                "name": "Western Wall",
                "religion": "Judaism", "place_type": "Synagogue",
                "address": "Western Wall Plaza", "city": "Jerusalem",
                "country_id": 5,
                "description": "The most sacred site in Judaism, the last remnant of the Second Temple.",
                "image_url": "https://images.unsplash.com/photo-1544274567-20f6d78ef90a?w=600",
                "latitude": 31.7767, "longitude": 35.2345,
            },
            {
                "name": "Kashi Vishwanath Temple",
                "religion": "Hinduism", "place_type": "Temple",
                "address": "Lahori Tola", "city": "Varanasi",
                "country_id": 4,
                "description": "One of the most famous Hindu temples dedicated to Lord Shiva.",
                "image_url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600",
                "latitude": 25.3109, "longitude": 83.0107,
            },
            {
                "name": "Westminster Abbey",
                "religion": "Christianity", "place_type": "Church",
                "address": "20 Deans Yd", "city": "London",
                "country_id": 2,
                "description": "A historic abbey church and coronation site for British monarchs.",
                "image_url": "https://images.unsplash.com/photo-1561489413-f35cb2d9a1f9?w=600",
                "latitude": 51.4994, "longitude": -0.1273,
            }
        ]

        for i, pd in enumerate(places_data):
            if db.query(PlaceOfWorship).filter(PlaceOfWorship.name == pd["name"]).first():
                continue
            
            owner = db.query(User).first() if i == 0 else None
            place = PlaceOfWorship(**pd, created_by=owner.id if owner else None)
            db.add(place)
            db.flush()

        db.commit()
    except Exception as e:
        print(f"Seeding skipped or failed: {e}")
    finally:
        db.close()
