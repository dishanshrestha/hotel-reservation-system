from __future__ import annotations

import datetime as dt
import os
import smtplib
import ssl
from decimal import Decimal
from email.message import EmailMessage
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import models
from services.image_service import _as_public_image_path
from services.room_service import _safe_float


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
