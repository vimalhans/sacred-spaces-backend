import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import seed

seed()

app = FastAPI(title="Global Places of Worship", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://sacredspaces.world",
        "https://sacred-spaces-app.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.auth import router as auth_router
from routes.countries import router as countries_router
from routes.places import router as places_router
from routes.events import router as events_router
from routes.prayer_times import router as prayer_times_router
from routes.stripe_api import router as stripe_router

app.include_router(auth_router)
app.include_router(countries_router)
app.include_router(places_router)
app.include_router(events_router)
app.include_router(prayer_times_router)
app.include_router(stripe_router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
