from __future__ import annotations

import datetime as dt
import heapq
import os
import smtplib
import ssl
import shutil
import uuid
from decimal import Decimal
from email.message import EmailMessage
from pathlib import Path
from typing import Annotated, Any

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field, model_validator
from sqlalchemy import func
from sqlalchemy.orm import Session

load_dotenv(Path(__file__).resolve().parent / ".env")

import models
from auth import (
    create_access_token,
    get_current_admin,
    get_current_user,
    get_optional_user,
    get_password_hash,
    verify_password,
)
from database import Base, engine, get_db


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    usertype: str
    profile_photo_path: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserPublic


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
    phone: str | None = Field(default=None, max_length=255)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=255)


class PasswordUpdateRequest(BaseModel):
    current_password: str
    password: str = Field(min_length=8, max_length=255)
    password_confirmation: str

    @model_validator(mode="after")
    def validate_password_confirmation(self) -> "PasswordUpdateRequest":
        if self.password != self.password_confirmation:
            raise ValueError("Password confirmation does not match")
        return self


class BookingCreateRequest(BaseModel):
    room_id: int
    start_date: dt.date
    end_date: dt.date
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=255)
    total_price: Decimal | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingCreateRequest":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class BookingCreateByRoomRequest(BaseModel):
    start_date: dt.date
    end_date: dt.date
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=255)
    total_price: Decimal | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingCreateByRoomRequest":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class CheckoutRequest(BaseModel):
    room_id: int
    start_date: dt.date
    end_date: dt.date
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    phone: str = Field(min_length=1, max_length=255)
    total_price: Decimal = Field(gt=0)

    @model_validator(mode="after")
    def validate_dates(self) -> "CheckoutRequest":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class BookingStatusRequest(BaseModel):
    status: str


class ContactRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    phone: str = Field(min_length=1, max_length=255)
    message: str = Field(min_length=1)


class RatingRequest(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    comment: str = Field(min_length=1, max_length=255)
    rating: int = Field(ge=1, le=5)


class AdminUserUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=255)
    usertype: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=255)


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

MEDIA_DIR = Path(__file__).resolve().parent / "media"


def _as_public_image_path(value: str | None) -> str | None:
    if not value:
        return value
    stripped = value.strip()
    if stripped.startswith(("http://", "https://", "/")):
        return stripped
    return f"/media/{stripped.lstrip('/')}"


MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")


@app.on_event("startup")
def startup() -> None:
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)


def _serialize_user(user: models.User) -> dict[str, Any]:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "usertype": user.usertype,
        "profile_photo_path": user.profile_photo_path,
    }


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _serialize_room(db: Session, room: models.Room, include_ratings: bool = False) -> dict[str, Any]:
    avg_rating, rating_count = (
        db.query(func.avg(models.RoomRating.rating), func.count(models.RoomRating.id))
        .filter(models.RoomRating.room_id == room.id, models.RoomRating.status == 1)
        .one()
    )

    data = {
        "id": room.id,
        "room_title": room.room_title,
        "image": _as_public_image_path(room.image),
        "image_raw": room.image,
        "description": room.description,
        "price": room.price,
        "wifi": room.wifi,
        "room_type": room.room_type,
        "created_at": room.created_at,
        "updated_at": room.updated_at,
        "average_rating": round(float(avg_rating or 0), 2),
        "rating_count": int(rating_count or 0),
    }

    if include_ratings:
        ratings = (
            db.query(models.RoomRating)
            .filter(models.RoomRating.room_id == room.id, models.RoomRating.status == 1)
            .order_by(models.RoomRating.created_at.desc())
            .all()
        )
        data["ratings"] = [
            {
                "id": rating.id,
                "username": rating.username,
                "email": rating.email,
                "comment": rating.comment,
                "rating": float(rating.rating),
                "created_at": rating.created_at,
            }
            for rating in ratings
        ]

    return data


def _serialize_booking(db: Session, booking: models.Booking) -> dict[str, Any]:
    room_title = None
    room_image = None
    if booking.room_id and str(booking.room_id).isdigit():
        room = db.get(models.Room, int(booking.room_id))
        if room:
            room_title = room.room_title
            room_image = room.image

    return {
        "id": booking.id,
        "room_id": booking.room_id,
        "room_title": room_title,
        "room_image": _as_public_image_path(room_image),
        "name": booking.name,
        "email": booking.email,
        "phone": booking.phone,
        "status": booking.status,
        "start_date": booking.start_date,
        "end_date": booking.end_date,
        "total_price": _safe_float(booking.total_price),
        "created_at": booking.created_at,
        "updated_at": booking.updated_at,
    }


def _room_exists(db: Session, room_id: int) -> bool:
    return db.get(models.Room, room_id) is not None


def _booking_overlaps(db: Session, room_id: int, start_date: dt.date, end_date: dt.date) -> bool:
    overlapping = (
        db.query(models.Booking)
        .filter(
            models.Booking.room_id == str(room_id),
            models.Booking.start_date <= end_date.isoformat(),
            models.Booking.end_date >= start_date.isoformat(),
        )
        .first()
    )
    return overlapping is not None


def _parse_booking_date(value: str | None) -> dt.date | None:
    if not value:
        return None
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


def _collect_room_booking_intervals(db: Session, room_id: int) -> list[tuple[dt.date, dt.date]]:
    records = (
        db.query(models.Booking.start_date, models.Booking.end_date)
        .filter(models.Booking.room_id == str(room_id))
        .all()
    )

    intervals: list[tuple[dt.date, dt.date]] = []
    for start_raw, end_raw in records:
        start_date = _parse_booking_date(start_raw)
        end_date = _parse_booking_date(end_raw)
        if not start_date or not end_date or end_date < start_date:
            continue
        intervals.append((start_date, end_date))

    intervals.sort(key=lambda item: item[0])
    return intervals


def _merge_booking_intervals(intervals: list[tuple[dt.date, dt.date]]) -> list[tuple[dt.date, dt.date]]:
    if not intervals:
        return []

    merged: list[list[dt.date]] = [[intervals[0][0], intervals[0][1]]]
    for start_date, end_date in intervals[1:]:
        last_start, last_end = merged[-1]
        if start_date <= (last_end + dt.timedelta(days=1)):
            merged[-1][1] = max(last_end, end_date)
        else:
            merged.append([start_date, end_date])

    return [(item[0], item[1]) for item in merged]


def _find_next_available_slots(
    db: Session,
    room_id: int,
    requested_start: dt.date,
    requested_end: dt.date,
    max_suggestions: int = 3,
    lookahead_days: int = 180,
) -> list[dict[str, Any]]:
    stay_nights = max(1, (requested_end - requested_start).days)
    horizon = requested_start + dt.timedelta(days=lookahead_days)

    intervals = _merge_booking_intervals(_collect_room_booking_intervals(db, room_id))

    suggestions: list[dict[str, Any]] = []
    cursor = requested_start

    for interval_start, interval_end in intervals:
        if len(suggestions) >= max_suggestions or cursor > horizon:
            break

        latest_start_before_interval = interval_start - dt.timedelta(days=stay_nights + 1)
        while cursor <= latest_start_before_interval and len(suggestions) < max_suggestions and cursor <= horizon:
            suggestion_end = cursor + dt.timedelta(days=stay_nights)
            suggestions.append(
                {
                    "start_date": cursor.isoformat(),
                    "end_date": suggestion_end.isoformat(),
                    "nights": stay_nights,
                }
            )
            cursor = suggestion_end + dt.timedelta(days=1)

        if cursor <= interval_end:
            cursor = interval_end + dt.timedelta(days=1)

    while len(suggestions) < max_suggestions and cursor <= horizon:
        suggestion_end = cursor + dt.timedelta(days=stay_nights)
        suggestions.append(
            {
                "start_date": cursor.isoformat(),
                "end_date": suggestion_end.isoformat(),
                "nights": stay_nights,
            }
        )
        cursor = suggestion_end + dt.timedelta(days=1)

    return suggestions


def _as_bool_flag(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "required", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return None


def _wifi_available(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"yes", "true", "1", "available"}


def _recommend_rooms_for_stay(
    db: Session,
    rooms: list[dict[str, Any]],
    start_date: dt.date | None,
    end_date: dt.date | None,
    room_type: str | None,
    max_budget: float | None,
    wifi_required: bool | None,
    top_k: int,
) -> list[dict[str, Any]]:
    available_rooms: list[dict[str, Any]] = []
    price_values: list[float] = []

    for room in rooms:
        room_id = int(room["id"])
        if start_date and end_date and _booking_overlaps(db, room_id, start_date, end_date):
            continue
        available_rooms.append(room)
        room_price = _safe_float(room.get("price"))
        if room_price is not None:
            price_values.append(room_price)

    if not available_rooms:
        return []

    min_price = min(price_values) if price_values else None
    max_price = max(price_values) if price_values else None

    scored_items: list[tuple[float, dict[str, Any]]] = []
    for room in available_rooms:
        room_price = _safe_float(room.get("price"))
        rating_score = min(1.0, max(0.0, float(room.get("average_rating") or 0) / 5.0))

        if max_budget is not None:
            if room_price is None:
                price_score = 0.35
            elif room_price <= max_budget:
                affordability = max(0.0, 1.0 - (room_price / max_budget))
                price_score = 0.55 + (0.45 * affordability)
            else:
                over_budget = (room_price - max_budget) / max_budget
                price_score = max(0.0, 0.4 - over_budget)
        else:
            if room_price is None or min_price is None or max_price is None:
                price_score = 0.5
            elif max_price == min_price:
                price_score = 1.0
            else:
                price_score = 1.0 - ((room_price - min_price) / (max_price - min_price))

        if room_type:
            type_score = 1.0 if str(room.get("room_type") or "").strip().lower() == room_type.strip().lower() else 0.0
        else:
            type_score = 0.5

        room_wifi = _wifi_available(room.get("wifi"))
        if wifi_required is True:
            wifi_score = 1.0 if room_wifi else 0.0
        elif wifi_required is False:
            wifi_score = 1.0 if not room_wifi else 0.6
        else:
            wifi_score = 0.5

        weighted_score = (
            (0.42 * rating_score)
            + (0.28 * price_score)
            + (0.20 * type_score)
            + (0.10 * wifi_score)
        )

        reasons = [
            f"rating={round(rating_score * 100, 1)}%",
            f"price-fit={round(price_score * 100, 1)}%",
            f"type-fit={round(type_score * 100, 1)}%",
            f"wifi-fit={round(wifi_score * 100, 1)}%",
        ]

        scored_items.append(
            (
                weighted_score,
                {
                    **room,
                    "recommendation_score": round(weighted_score, 4),
                    "recommendation_reasons": reasons,
                },
            )
        )

    best = heapq.nlargest(top_k, scored_items, key=lambda item: item[0])
    return [item[1] for item in best]


def _create_booking(
    db: Session,
    room_id: int,
    start_date: dt.date,
    end_date: dt.date,
    name: str | None,
    email: str | None,
    phone: str | None,
    total_price: Decimal | None,
    status_value: str,
    current_user: models.User | None,
) -> models.Booking:
    if not _room_exists(db, room_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    if _booking_overlaps(db, room_id, start_date, end_date):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room is already booked for the selected dates",
        )

    resolved_name = name or (current_user.name if current_user else None)
    resolved_email = email or (current_user.email if current_user else None)

    if not resolved_name or not resolved_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="name and email are required",
        )

    booking = models.Booking(
        room_id=str(room_id),
        name=resolved_name,
        email=resolved_email,
        phone=phone,
        total_price=total_price,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        status=status_value,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def _bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _send_booking_confirmation_email(booking_data: dict[str, Any]) -> tuple[bool, str]:
    recipient = str(booking_data.get("email") or "").strip()
    if not recipient:
        return False, "Booking email is missing"

    smtp_host = os.getenv("SMTP_HOST", "").strip()
    if not smtp_host:
        return False, "SMTP is not configured"

    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "").strip()
    smtp_sender = os.getenv("SMTP_SENDER", smtp_username or "no-reply@localhost").strip()
    use_tls = _bool_env("SMTP_USE_TLS", True)

    room_label = booking_data.get("room_title") or f"Room #{booking_data.get('room_id')}"
    booking_id = booking_data.get("id")

    subject = f"Booking Confirmation #{booking_id}"
    body = (
        "Your hotel booking has been received.\n\n"
        f"Booking ID: {booking_id}\n"
        f"Room: {room_label}\n"
        f"Guest Name: {booking_data.get('name') or '-'}\n"
        f"Check-in: {booking_data.get('start_date') or '-'}\n"
        f"Check-out: {booking_data.get('end_date') or '-'}\n"
        f"Status: {booking_data.get('status') or '-'}\n"
        f"Total Price: {booking_data.get('total_price') or '-'}\n\n"
        "Thank you for choosing our hotel."
    )

    message = EmailMessage()
    message["From"] = smtp_sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            if use_tls:
                server.starttls(context=ssl.create_default_context())
            if smtp_username and smtp_password:
                server.login(smtp_username, smtp_password)
            server.send_message(message)
        return True, "Confirmation email sent"
    except Exception as exc:
        return False, f"Failed to send email: {exc}"


def _save_upload(file: UploadFile, sub_dir: str) -> str:
    folder = MEDIA_DIR / sub_dir
    folder.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename or "").suffix
    filename = f"{int(dt.datetime.utcnow().timestamp())}_{uuid.uuid4().hex[:8]}{extension}"
    destination = folder / filename

    with destination.open("wb") as output:
        shutil.copyfileobj(file.file, output)

    return f"{sub_dir}/{filename}"


def _filter_rooms(
    db: Session,
    price_range: str | None,
    room_type: str | None,
) -> list[dict[str, Any]]:
    min_price = None
    max_price = None

    if price_range:
        if "-" not in price_range:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="price_range must follow the format 'min-max'",
            )
        parts = price_range.split("-", maxsplit=1)
        try:
            min_price = float(parts[0])
            max_price = float(parts[1])
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="price_range contains invalid numeric values",
            ) from exc

    rooms = db.query(models.Room).order_by(models.Room.created_at.desc()).all()
    output = []

    for room in rooms:
        if room_type and (room.room_type or "") != room_type:
            continue

        if min_price is not None and max_price is not None:
            room_price = _safe_float(room.price)
            if room_price is None:
                continue
            if not (min_price <= room_price <= max_price):
                continue

        output.append(_serialize_room(db, room))

    return output


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hotel Reservation Python API is running"}


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/auth/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = models.User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        usertype="user",
        password=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _serialize_user(user)


@app.post("/api/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if user is None or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.usertype})
    return {"access_token": token, "token_type": "bearer", "user": _serialize_user(user)}


@app.post("/api/auth/token", response_model=TokenResponse)
def login_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.usertype})
    return {"access_token": token, "token_type": "bearer", "user": _serialize_user(user)}


@app.get("/api/profile", response_model=UserPublic)
def get_profile(current_user: models.User = Depends(get_current_user)):
    return _serialize_user(current_user)


@app.put("/api/profile", response_model=UserPublic)
def update_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if payload.email and payload.email != current_user.email:
        exists = db.query(models.User).filter(models.User.email == payload.email).first()
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        current_user.email = payload.email

    if payload.name is not None:
        current_user.name = payload.name
    if payload.phone is not None:
        current_user.phone = payload.phone

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return _serialize_user(current_user)


@app.put("/api/profile/password")
def update_profile_password(
    payload: PasswordUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not verify_password(payload.current_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

    current_user.password = get_password_hash(payload.password)
    db.add(current_user)
    db.commit()
    return {"message": "Password updated successfully"}


@app.put("/api/settings", response_model=UserPublic)
def update_settings(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return update_profile(payload=payload, db=db, current_user=current_user)


@app.get("/api/rooms")
def list_rooms(
    price_range: str | None = Query(default=None),
    room_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    rooms = _filter_rooms(db, price_range, room_type)
    return {"count": len(rooms), "rooms": rooms}


@app.get("/api/our_rooms")
def our_rooms(
    price_range: str | None = Query(default=None),
    room_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return list_rooms(price_range=price_range, room_type=room_type, db=db)


@app.get("/api/search-rooms")
def search_rooms(
    price_range: str | None = Query(default=None),
    room_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return list_rooms(price_range=price_range, room_type=room_type, db=db)


@app.get("/api/rooms/{room_id}")
def room_details(room_id: int, db: Session = Depends(get_db)):
    room = db.get(models.Room, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return _serialize_room(db, room, include_ratings=True)


@app.get("/api/room_details/{room_id}")
def legacy_room_details(room_id: int, db: Session = Depends(get_db)):
    return room_details(room_id=room_id, db=db)


@app.get("/api/recommendations/rooms")
def recommend_rooms(
    start_date: dt.date | None = Query(default=None),
    end_date: dt.date | None = Query(default=None),
    room_type: str | None = Query(default=None),
    max_budget: float | None = Query(default=None, gt=0),
    wifi: str | None = Query(default=None),
    top_k: int = Query(default=3, ge=1, le=10),
    db: Session = Depends(get_db),
):
    if (start_date is None) ^ (end_date is None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide both start_date and end_date")

    if start_date and end_date and end_date <= start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="end_date must be after start_date")

    wifi_required = _as_bool_flag(wifi)
    all_rooms = _filter_rooms(db, price_range=None, room_type=None)
    recommendations = _recommend_rooms_for_stay(
        db=db,
        rooms=all_rooms,
        start_date=start_date,
        end_date=end_date,
        room_type=room_type,
        max_budget=max_budget,
        wifi_required=wifi_required,
        top_k=top_k,
    )

    return {
        "count": len(recommendations),
        "algorithm": "weighted-multi-factor-top-k",
        "recommendations": recommendations,
    }


@app.get("/api/rooms/{room_id}/availability-suggestions")
def room_availability_suggestions(
    room_id: int,
    start_date: dt.date,
    end_date: dt.date,
    max_suggestions: int = Query(default=3, ge=1, le=10),
    db: Session = Depends(get_db),
):
    if end_date <= start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="end_date must be after start_date")

    if not _room_exists(db, room_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    suggestions = _find_next_available_slots(
        db=db,
        room_id=room_id,
        requested_start=start_date,
        requested_end=end_date,
        max_suggestions=max_suggestions,
    )
    return {
        "room_id": room_id,
        "requested_start_date": start_date.isoformat(),
        "requested_end_date": end_date.isoformat(),
        "count": len(suggestions),
        "algorithm": "merged-interval-gap-scan",
        "alternative_slots": suggestions,
    }


@app.post("/api/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(
    payload: BookingCreateRequest,
    db: Session = Depends(get_db),
    current_user: models.User | None = Depends(get_optional_user),
):
    try:
        booking = _create_booking(
            db=db,
            room_id=payload.room_id,
            start_date=payload.start_date,
            end_date=payload.end_date,
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            total_price=payload.total_price,
            status_value="waiting",
            current_user=current_user,
        )
    except HTTPException as exc:
        if exc.status_code == status.HTTP_409_CONFLICT:
            alternatives = _find_next_available_slots(
                db=db,
                room_id=payload.room_id,
                requested_start=payload.start_date,
                requested_end=payload.end_date,
                max_suggestions=3,
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "Room is already booked for the selected dates",
                    "alternative_slots": alternatives,
                },
            ) from exc
        raise

    booking_data = _serialize_booking(db, booking)
    email_sent, email_message = _send_booking_confirmation_email(booking_data)
    return {
        "message": "Room booked successfully",
        "booking": booking_data,
        "email_confirmation_sent": email_sent,
        "email_confirmation_message": email_message,
    }


@app.post("/api/add_booking/{room_id}", status_code=status.HTTP_201_CREATED)
def create_booking_legacy(
    room_id: int,
    payload: BookingCreateByRoomRequest,
    db: Session = Depends(get_db),
    current_user: models.User | None = Depends(get_optional_user),
):
    try:
        booking = _create_booking(
            db=db,
            room_id=room_id,
            start_date=payload.start_date,
            end_date=payload.end_date,
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            total_price=payload.total_price,
            status_value="waiting",
            current_user=current_user,
        )
    except HTTPException as exc:
        if exc.status_code == status.HTTP_409_CONFLICT:
            alternatives = _find_next_available_slots(
                db=db,
                room_id=room_id,
                requested_start=payload.start_date,
                requested_end=payload.end_date,
                max_suggestions=3,
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "Room is already booked for the selected dates",
                    "alternative_slots": alternatives,
                },
            ) from exc
        raise

    booking_data = _serialize_booking(db, booking)
    email_sent, email_message = _send_booking_confirmation_email(booking_data)
    return {
        "message": "Room booked successfully",
        "booking": booking_data,
        "email_confirmation_sent": email_sent,
        "email_confirmation_message": email_message,
    }


@app.get("/api/bookings/me")
def my_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    records = (
        db.query(models.Booking)
        .filter(models.Booking.email == current_user.email)
        .order_by(models.Booking.created_at.desc())
        .all()
    )
    return {"count": len(records), "bookings": [_serialize_booking(db, booking) for booking in records]}


@app.get("/api/mybooking")
def my_bookings_legacy(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return my_bookings(db=db, current_user=current_user)


@app.patch("/api/bookings/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    booking = db.get(models.Booking, booking_id)
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    if current_user.usertype.lower() != "admin" and booking.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    booking.status = "canceled"
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return {"message": "Booking canceled", "booking": _serialize_booking(db, booking)}


@app.post("/api/checkout", status_code=status.HTTP_201_CREATED)
def checkout(
    payload: CheckoutRequest,
    db: Session = Depends(get_db),
):
    booking = _create_booking(
        db=db,
        room_id=payload.room_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        total_price=payload.total_price,
        status_value="paid",
        current_user=None,
    )
    return {
        "message": "Checkout completed and booking marked as paid",
        "booking": _serialize_booking(db, booking),
    }


@app.post("/api/webhook", status_code=status.HTTP_201_CREATED)
def webhook_booking(payload: BookingCreateRequest, db: Session = Depends(get_db)):
    booking = _create_booking(
        db=db,
        room_id=payload.room_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        total_price=payload.total_price,
        status_value="waiting",
        current_user=None,
    )
    return {"message": "Webhook booking stored", "booking": _serialize_booking(db, booking)}


@app.post("/api/contact", status_code=status.HTTP_201_CREATED)
def create_contact(payload: ContactRequest, db: Session = Depends(get_db)):
    contact = models.Contact(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        message=payload.message,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return {"message": "Message sent successfully", "contact_id": contact.id}


@app.get("/api/gallery")
def list_gallery(db: Session = Depends(get_db)):
    items = db.query(models.Gallary).order_by(models.Gallary.created_at.desc()).all()
    return {
        "count": len(items),
        "gallery": [
            {
                "id": item.id,
                "image": _as_public_image_path(item.image),
                "image_raw": item.image,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ],
    }


@app.get("/api/hotel_gallary")
def list_gallery_legacy(db: Session = Depends(get_db)):
    return list_gallery(db=db)


@app.post("/api/ratings/{room_id}", status_code=status.HTTP_201_CREATED)
def save_rating(room_id: int, payload: RatingRequest, db: Session = Depends(get_db)):
    room = db.get(models.Room, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    duplicate = (
        db.query(models.RoomRating)
        .filter(models.RoomRating.room_id == room_id, models.RoomRating.email == payload.email)
        .count()
    )
    if duplicate > 0:
        return {"status": "duplicate", "message": "You already rated this Room"}

    room_rating = models.RoomRating(
        room_id=room_id,
        username=payload.name,
        email=payload.email,
        comment=payload.comment,
        rating=payload.rating,
        status=1,
    )
    db.add(room_rating)
    db.commit()
    db.refresh(room_rating)

    return {"status": True, "message": "Thanks for your rating.", "rating_id": room_rating.id}


@app.post("/api/save-rating/{room_id}", status_code=status.HTTP_201_CREATED)
def save_rating_legacy(room_id: int, payload: RatingRequest, db: Session = Depends(get_db)):
    return save_rating(room_id=room_id, payload=payload, db=db)


@app.get("/api/admin/stats")
def admin_stats(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    total_users = db.query(func.count(models.User.id)).scalar() or 0
    total_bookings = db.query(func.count(models.Booking.id)).scalar() or 0
    total_rooms = db.query(func.count(models.Room.id)).scalar() or 0

    bookings = db.query(models.Booking).all()
    rejected_count = 0
    canceled_count = 0
    approved_count = 0
    waiting_count = 0
    total_income = 0.0

    monthly_counts = [0] * 12
    current_year = dt.datetime.utcnow().year

    for booking in bookings:
        status_lower = (booking.status or "").strip().lower()
        if status_lower == "rejected":
            rejected_count += 1
        elif status_lower in {"canceled", "cancelled"}:
            canceled_count += 1
        elif status_lower in {"approve", "approved", "paid"}:
            approved_count += 1
        elif status_lower == "waiting":
            waiting_count += 1

        if booking.total_price is not None:
            total_income += float(booking.total_price)

        if booking.created_at and booking.created_at.year == current_year:
            monthly_counts[booking.created_at.month - 1] += 1

    labels = [dt.date(2000, month, 1).strftime("%B") for month in range(1, 13)]

    return {
        "total_users": int(total_users),
        "total_bookings": int(total_bookings),
        "total_rooms": int(total_rooms),
        "total_income": round(total_income, 2),
        "status_counts": {
            "rejected": rejected_count,
            "canceled": canceled_count,
            "approved": approved_count,
            "waiting": waiting_count,
        },
        "bookings_by_month": {
            "labels": labels,
            "data": monthly_counts,
        },
    }


@app.get("/api/admin/rooms")
def admin_list_rooms(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    rooms = db.query(models.Room).order_by(models.Room.created_at.desc()).all()
    return {"count": len(rooms), "rooms": [_serialize_room(db, room) for room in rooms]}


@app.post("/api/admin/rooms", status_code=status.HTTP_201_CREATED)
def admin_create_room(
    room_title: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    price: Annotated[str | None, Form()] = None,
    wifi: Annotated[str | None, Form()] = "yes",
    room_type: Annotated[str | None, Form()] = None,
    image: Annotated[str | None, Form()] = None,
    image_url: Annotated[str | None, Form()] = None,
    image_file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    image_path = image_url or image
    if image_file is not None:
        image_path = _save_upload(image_file, "rooms")

    room = models.Room(
        room_title=room_title,
        description=description,
        price=price,
        wifi=wifi or "yes",
        room_type=room_type,
        image=image_path,
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return _serialize_room(db, room)


@app.put("/api/admin/rooms/{room_id}")
def admin_update_room(
    room_id: int,
    room_title: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    price: Annotated[str | None, Form()] = None,
    wifi: Annotated[str | None, Form()] = None,
    room_type: Annotated[str | None, Form()] = None,
    image: Annotated[str | None, Form()] = None,
    image_url: Annotated[str | None, Form()] = None,
    image_file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    room = db.get(models.Room, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    if room_title is not None:
        room.room_title = room_title
    if description is not None:
        room.description = description
    if price is not None:
        room.price = price
    if wifi is not None:
        room.wifi = wifi
    if room_type is not None:
        room.room_type = room_type
    if image is not None:
        room.image = image
    if image_url is not None:
        room.image = image_url
    if image_file is not None:
        room.image = _save_upload(image_file, "rooms")

    db.add(room)
    db.commit()
    db.refresh(room)
    return _serialize_room(db, room)


@app.delete("/api/admin/rooms/{room_id}")
def admin_delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    room = db.get(models.Room, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    db.delete(room)
    db.commit()
    return {"message": "Room deleted"}


@app.get("/api/admin/bookings")
def admin_list_bookings(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    bookings = db.query(models.Booking).order_by(models.Booking.created_at.desc()).all()
    return {"count": len(bookings), "bookings": [_serialize_booking(db, booking) for booking in bookings]}


@app.patch("/api/admin/bookings/{booking_id}/status")
def admin_update_booking_status(
    booking_id: int,
    payload: BookingStatusRequest,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    booking = db.get(models.Booking, booking_id)
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    allowed = {"waiting", "approve", "approved", "rejected", "canceled", "cancelled", "paid"}
    new_status = payload.status.strip().lower()
    if new_status not in allowed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")

    booking.status = new_status
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return {"message": "Booking status updated", "booking": _serialize_booking(db, booking)}


@app.delete("/api/admin/bookings/{booking_id}")
def admin_delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    booking = db.get(models.Booking, booking_id)
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted"}


@app.get("/api/admin/contacts")
def admin_list_contacts(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    contacts = db.query(models.Contact).order_by(models.Contact.created_at.desc()).all()
    return {
        "count": len(contacts),
        "contacts": [
            {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
                "message": contact.message,
                "created_at": contact.created_at,
                "updated_at": contact.updated_at,
            }
            for contact in contacts
        ],
    }


@app.get("/api/admin/messages")
def admin_list_messages(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    return admin_list_contacts(db=db, _admin=_admin)


@app.get("/api/admin/users")
def admin_list_users(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return {"count": len(users), "users": [_serialize_user(user) for user in users]}


@app.get("/api/admin/gallery")
def admin_list_gallery(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    items = db.query(models.Gallary).order_by(models.Gallary.created_at.desc()).all()
    return {
        "count": len(items),
        "gallery": [
            {
                "id": item.id,
                "image": _as_public_image_path(item.image),
                "image_raw": item.image,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ],
    }


@app.put("/api/admin/users/{user_id}", response_model=UserPublic)
def admin_update_user(
    user_id: int,
    payload: AdminUserUpdateRequest,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    user = db.get(models.User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if payload.email and payload.email != user.email:
        email_owner = db.query(models.User).filter(models.User.email == payload.email).first()
        if email_owner:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        user.email = payload.email

    if payload.name is not None:
        user.name = payload.name
    if payload.phone is not None:
        user.phone = payload.phone
    if payload.usertype is not None:
        user.usertype = payload.usertype
    if payload.password is not None:
        user.password = get_password_hash(payload.password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return _serialize_user(user)


@app.delete("/api/admin/users/{user_id}")
def admin_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    user = db.get(models.User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


@app.post("/api/admin/gallery", status_code=status.HTTP_201_CREATED)
def admin_create_gallery(
    image: Annotated[str | None, Form()] = None,
    image_url: Annotated[str | None, Form()] = None,
    image_file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    image_path = image_url or image
    if image_file is not None:
        image_path = _save_upload(image_file, "gallery")

    if not image_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="image_url or image_file is required",
        )

    gallery = models.Gallary(image=image_path)
    db.add(gallery)
    db.commit()
    db.refresh(gallery)

    return {
        "id": gallery.id,
        "image": _as_public_image_path(gallery.image),
        "image_raw": gallery.image,
        "created_at": gallery.created_at,
        "updated_at": gallery.updated_at,
    }


@app.delete("/api/admin/gallery/{gallery_id}")
def admin_delete_gallery(
    gallery_id: int,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    gallery = db.get(models.Gallary, gallery_id)
    if gallery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery item not found")

    db.delete(gallery)
    db.commit()
    return {"message": "Gallery image deleted"}