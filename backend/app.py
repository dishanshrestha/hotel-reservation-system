from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

load_dotenv(Path(__file__).resolve().parent / ".env")

from database import Base, engine
from routers.admin_router import router as admin_router
from routers.auth_router import router as auth_router
from routers.bookings_router import router as bookings_router
from routers.contacts_router import router as contacts_router
from routers.gallery_router import router as gallery_router
from routers.profile_router import router as profile_router
from routers.ratings_router import router as ratings_router
from routers.blogs_router import router as blogs_router
from routers.rooms_router import router as rooms_router
from services.image_service import MEDIA_DIR

app = FastAPI(title="Hotel Reservation API", version="1.0.0")

cors_origins = os.getenv("CORS_ORIGINS", "*").strip()
allow_origins = ["*"] if cors_origins == "*" else [x.strip() for x in cors_origins.split(",") if x.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(gallery_router)
app.include_router(contacts_router)
app.include_router(ratings_router)
app.include_router(blogs_router)
app.include_router(admin_router)


@app.on_event("startup")
def startup() -> None:
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hotel Reservation Python API is running"}


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
