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
    Base.metadata.create_all(bind=engine)
    db = Session(engine)

    # Simple migration: add denomination column if it doesn't exist
    try:
        from sqlalchemy import text
        db.execute(text("ALTER TABLE places_of_worship ADD COLUMN denomination TEXT"))
        db.commit()
    except Exception:
        pass # Already exists or table not created yet

    if db.query(Country).count() > 30: # Use 30 to allow adding more countries
        db.close()
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
        db.add(Country(code=code, name=name))
    db.flush()

    def c(name):
        return db.query(Country).filter(Country.name == name).first()

    # Create a demo user with a placeholder place first
    demo_user = User(email="demo@worshipapp.com", password_hash=hash_password("demo123"))
    db.add(demo_user)
    db.flush()

    places_data = [
        {
            "name": "St. Peter's Basilica",
            "religion": "Christianity", "place_type": "Church",
            "address": "Piazza San Pietro", "city": "Vatican City",
            "country_id": c("Italy").id,
            "description": "One of the largest churches in the world and the center of the Catholic faith.",
            "image_url": "https://images.unsplash.com/photo-1555991780-4c6a1ef2a7a7?w=600",
            "latitude": 41.9022, "longitude": 12.4539,
        },
        {
            "name": "Masjid al-Haram",
            "religion": "Islam", "place_type": "Mosque",
            "address": "Al Haram", "city": "Mecca",
            "country_id": c("Saudi Arabia").id,
            "description": "The holiest mosque in Islam, surrounding the Kaaba.",
            "image_url": "https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?w=600",
            "latitude": 21.4225, "longitude": 39.8262,
        },
        {
            "name": "Western Wall",
            "religion": "Judaism", "place_type": "Synagogue",
            "address": "Western Wall Plaza", "city": "Jerusalem",
            "country_id": c("Israel").id,
            "description": "The most sacred site in Judaism, the last remnant of the Second Temple.",
            "image_url": "https://images.unsplash.com/photo-1544274567-20f6d78ef90a?w=600",
            "latitude": 31.7767, "longitude": 35.2345,
        },
        {
            "name": "Kashi Vishwanath Temple",
            "religion": "Hinduism", "place_type": "Temple",
            "address": "Lahori Tola", "city": "Varanasi",
            "country_id": c("India").id,
            "description": "One of the most famous Hindu temples dedicated to Lord Shiva.",
            "image_url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600",
            "latitude": 25.3109, "longitude": 83.0107,
        },
        {
            "name": "Westminster Abbey",
            "religion": "Christianity", "place_type": "Church",
            "address": "20 Deans Yd", "city": "London",
            "country_id": c("United Kingdom").id,
            "description": "A historic abbey church and coronation site for British monarchs.",
            "image_url": "https://images.unsplash.com/photo-1561489413-f35cb2d9a1f9?w=600",
            "latitude": 51.4994, "longitude": -0.1273,
        },
        {
            "name": "Sultan Ahmed Mosque",
            "religion": "Islam", "place_type": "Mosque",
            "address": "Sultan Ahmet Mahallesi", "city": "Istanbul",
            "country_id": c("Turkey").id,
            "description": "The Blue Mosque, famous for its six minarets and blue Iznik tiles.",
            "image_url": "https://images.unsplash.com/photo-1604897320610-b99e9c3e2b3e?w=600",
            "latitude": 41.0054, "longitude": 28.9768,
        },
        {
            "name": "Shwedagon Pagoda",
            "religion": "Buddhism", "place_type": "Temple",
            "address": "Sang Zaung Chaung", "city": "Yangon",
            "country_id": c("Thailand").id,  # closest in our list
            "description": "A 2,500-year-old golden pagoda, the most sacred site in Myanmar.",
            "image_url": "https://images.unsplash.com/photo-1569747474860-30ad6b2e4b80?w=600",
            "latitude": 16.7983, "longitude": 96.1496,
        },
        {
            "name": "Cathedral of Notre-Dame",
            "religion": "Christianity", "place_type": "Church",
            "address": "6 Parvis Notre-Dame", "city": "Paris",
            "country_id": c("France").id,
            "description": "Iconic Gothic cathedral on the Ile de la Cite, recently restored.",
            "image_url": "https://images.unsplash.com/photo-1478391679764-b2d8b3cd1e94?w=600",
            "latitude": 48.8530, "longitude": 2.3499,
        },
        {
            "name": "Bodh Gaya Temple",
            "religion": "Buddhism", "place_type": "Temple",
            "address": "Bodh Gaya", "city": "Gaya",
            "country_id": c("India").id,
            "description": "The site where Buddha attained enlightenment under the Bodhi tree.",
            "image_url": "https://images.unsplash.com/photo-1600180758890-6b94519a8ba6?w=600",
            "latitude": 24.6959, "longitude": 84.9911,
        },
        {
            "name": "Great Synagogue of Rome",
            "religion": "Judaism", "place_type": "Synagogue",
            "address": "Lungotevere de' Cenci", "city": "Rome",
            "country_id": c("Italy").id,
            "description": "The largest synagogue in Rome, serving the Jewish community since 1904.",
            "image_url": "https://images.unsplash.com/photo-1601581875309-fafbf2d3ed3d?w=600",
            "latitude": 41.8919, "longitude": 12.4784,
        },
    ]

    for i, pd in enumerate(places_data):
        owner = db.query(User).first() if i == 0 else None
        place = PlaceOfWorship(**pd, created_by=owner.id if owner else None)
        db.add(place)
        db.flush()

        # Sample prayer times for religious places
        if pd["religion"] == "Islam":
            for pt in [
                ("Fajr", "05:30"), ("Dhuhr", "12:30"), ("Asr", "15:45"),
                ("Maghrib", "18:30"), ("Isha", "20:00"),
            ]:
                db.add(PrayerTime(place_id=place.id, prayer_name=pt[0], time=pt[1]))
        elif pd["religion"] == "Judaism":
            for pt in [("Shacharit", "08:00"), ("Mincha", "13:30"), ("Maariv", "19:00")]:
                db.add(PrayerTime(place_id=place.id, prayer_name=pt[0], time=pt[1]))

        # Sample events
        if i % 2 == 0:
            db.add(Event(
                place_id=place.id,
                title="Community Gathering",
                description="Weekly community meetup, all are welcome.",
                start_time=datetime(2026, 5, 10, 10, 0),
                end_time=datetime(2026, 5, 10, 12, 0),
                recurring=True,
            ))
        else:
            db.add(Event(
                place_id=place.id,
                title="Annual Festival",
                description="Annual celebration with music, food, and prayer.",
                start_time=datetime(2026, 6, 15, 9, 0),
                end_time=datetime(2026, 6, 15, 18, 0),
            ))

    db.commit()
    db.close()
