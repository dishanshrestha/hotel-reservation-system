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


def _get_smtp_config(db: Session | None = None) -> dict[str, Any]:
    """Load SMTP settings from DB first, then fall back to .env"""
    cfg: dict[str, Any] = {
        "host": os.getenv("SMTP_HOST", "").strip(),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "username": os.getenv("SMTP_USERNAME", "").strip(),
        "password": os.getenv("SMTP_PASSWORD", "").strip(),
        "sender": os.getenv("SMTP_SENDER", "").strip(),
        "use_tls": _bool_env("SMTP_USE_TLS", True),
    }

    if db is not None:
        try:
            from services.settings_service import get_smtp_settings
            db_cfg = get_smtp_settings(db)
            if db_cfg.get("smtp_host"):
                cfg["host"] = db_cfg["smtp_host"]
            if db_cfg.get("smtp_port"):
                try:
                    cfg["port"] = int(db_cfg["smtp_port"])
                except (TypeError, ValueError):
                    pass
            if db_cfg.get("smtp_username"):
                cfg["username"] = db_cfg["smtp_username"]
            if db_cfg.get("smtp_password"):
                cfg["password"] = db_cfg["smtp_password"]
            if db_cfg.get("smtp_sender"):
                cfg["sender"] = db_cfg["smtp_sender"]
            if db_cfg.get("smtp_use_tls") is not None:
                cfg["use_tls"] = db_cfg["smtp_use_tls"] in ("1", "true", "yes", "on", True)
        except Exception:
            pass

    if not cfg["sender"]:
        cfg["sender"] = cfg["username"] or "no-reply@localhost"

    return cfg


def _send_email(
    db: Session | None,
    recipient: str,
    subject: str,
    body: str,
) -> tuple[bool, str]:
    """Generic email sender using DB/env SMTP config."""
    if not recipient.strip():
        return False, "Recipient email is missing"

    cfg = _get_smtp_config(db)
    if not cfg["host"]:
        return False, "SMTP is not configured — set it in Admin > Settings"

    message = EmailMessage()
    message["From"] = cfg["sender"]
    message["To"] = recipient.strip()
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(cfg["host"], cfg["port"], timeout=20) as server:
            if cfg["use_tls"]:
                server.starttls(context=ssl.create_default_context())
            if cfg["username"] and cfg["password"]:
                server.login(cfg["username"], cfg["password"])
            server.send_message(message)
        return True, "Email sent"
    except Exception as exc:
        return False, f"Failed to send email: {exc}"


def _send_booking_confirmation_email(booking_data: dict[str, Any], db: Session | None = None) -> tuple[bool, str]:
    recipient = str(booking_data.get("email") or "").strip()
    if not recipient:
        return False, "Booking email is missing"

    room_label = booking_data.get("room_title") or f"Room #{booking_data.get('room_id')}"
    booking_id = booking_data.get("id")

    subject = f"Booking Confirmation #{booking_id} — StarterHotel"
    body = (
        "Dear {name},\n\n"
        "Your hotel booking has been received!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "  Booking Details\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "  Booking ID:  #{booking_id}\n"
        "  Room:        {room}\n"
        "  Check-in:    {checkin}\n"
        "  Check-out:   {checkout}\n"
        "  Total Price: ${price}\n"
        "  Status:      {status}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "We look forward to welcoming you at StarterHotel, Thamel, Kathmandu!\n\n"
        "If you have any questions, reply to this email or call us at +977 1-4700123.\n\n"
        "Warm regards,\n"
        "StarterHotel Team"
    ).format(
        name=booking_data.get("name") or "Guest",
        booking_id=booking_id,
        room=room_label,
        checkin=booking_data.get("start_date") or "-",
        checkout=booking_data.get("end_date") or "-",
        price=booking_data.get("total_price") or "-",
        status=booking_data.get("status") or "-",
    )

    return _send_email(db, recipient, subject, body)


def _send_contact_confirmation_email(contact_data: dict[str, Any], db: Session | None = None) -> tuple[bool, str]:
    recipient = str(contact_data.get("email") or "").strip()
    if not recipient:
        return False, "Contact email is missing"

    subject = "We received your message — StarterHotel"
    body = (
        "Dear {name},\n\n"
        "Thank you for contacting StarterHotel!\n\n"
        "We have received your message and will get back to you within 24 hours.\n\n"
        "Your message:\n"
        "─────────────────────────\n"
        "{message}\n"
        "─────────────────────────\n\n"
        "Warm regards,\n"
        "StarterHotel Team\n"
        "Thamel, Kathmandu 44600, Nepal\n"
        "+977 1-4700123"
    ).format(
        name=contact_data.get("name") or "Guest",
        message=contact_data.get("message") or "",
    )

    return _send_email(db, recipient, subject, body)
