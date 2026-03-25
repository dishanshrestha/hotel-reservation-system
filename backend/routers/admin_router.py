from __future__ import annotations

import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
from auth import get_current_admin, get_password_hash
from database import get_db
from schemas.admin import AdminUserUpdateRequest
from schemas.auth import UserPublic
from schemas.bookings import BookingStatusRequest
from services.booking_service import _serialize_booking
from services.image_service import _as_public_image_path, _save_upload
from services.room_service import _serialize_room
from services.user_service import _serialize_user
from services.settings_service import get_smtp_settings, save_smtp_settings
from services.booking_service import _send_email
from schemas.settings import SmtpSettingsRequest, TestEmailRequest

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
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


@router.get("/rooms")
def admin_list_rooms(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    rooms = db.query(models.Room).order_by(models.Room.created_at.desc()).all()
    return {"count": len(rooms), "rooms": [_serialize_room(db, room) for room in rooms]}


@router.post("/rooms", status_code=status.HTTP_201_CREATED)
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


@router.put("/rooms/{room_id}")
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


@router.delete("/rooms/{room_id}")
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


@router.get("/bookings")
def admin_list_bookings(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    bookings = db.query(models.Booking).order_by(models.Booking.created_at.desc()).all()
    return {"count": len(bookings), "bookings": [_serialize_booking(db, booking) for booking in bookings]}


@router.patch("/bookings/{booking_id}/status")
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


@router.delete("/bookings/{booking_id}")
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


@router.get("/contacts")
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


@router.get("/messages")
def admin_list_messages(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    return admin_list_contacts(db=db, _admin=_admin)


@router.get("/users")
def admin_list_users(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return {"count": len(users), "users": [_serialize_user(user) for user in users]}


@router.put("/users/{user_id}", response_model=UserPublic)
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


@router.delete("/users/{user_id}")
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


@router.get("/gallery")
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


@router.post("/gallery", status_code=status.HTTP_201_CREATED)
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


@router.delete("/gallery/{gallery_id}")
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


# ── SMTP Settings ──────────────────────────────────────────────


@router.get("/smtp-settings")
def admin_get_smtp_settings(
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    settings = get_smtp_settings(db)
    # Mask password for security
    if settings.get("smtp_password"):
        settings["smtp_password"] = "••••••••"
    return settings


@router.put("/smtp-settings")
def admin_update_smtp_settings(
    payload: SmtpSettingsRequest,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    data = payload.model_dump(exclude_none=True)
    # Don't overwrite password with mask
    if data.get("smtp_password") == "••••••••":
        del data["smtp_password"]
    save_smtp_settings(db, data)
    return {"message": "SMTP settings updated"}


@router.post("/smtp-test")
def admin_test_smtp(
    payload: TestEmailRequest,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    ok, msg = _send_email(
        db=db,
        recipient=payload.recipient,
        subject="SMTP Test — StarterHotel",
        body="This is a test email from your StarterHotel admin panel.\n\nIf you received this, your SMTP settings are working correctly!",
    )
    return {"success": ok, "message": msg}
