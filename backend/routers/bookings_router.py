from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from auth import get_current_user, get_optional_user
from database import get_db
from schemas.bookings import (
    BookingCreateByRoomRequest,
    BookingCreateRequest,
    CheckoutRequest,
)
from services.booking_service import (
    _create_booking,
    _find_next_available_slots,
    _send_booking_confirmation_email,
    _serialize_booking,
)

router = APIRouter(prefix="/api", tags=["bookings"])


@router.post("/bookings", status_code=status.HTTP_201_CREATED)
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


@router.post("/add_booking/{room_id}", status_code=status.HTTP_201_CREATED)
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


@router.get("/bookings/me")
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


@router.get("/mybooking")
def my_bookings_legacy(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return my_bookings(db=db, current_user=current_user)


@router.patch("/bookings/{booking_id}/cancel")
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


@router.post("/checkout", status_code=status.HTTP_201_CREATED)
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


@router.post("/webhook", status_code=status.HTTP_201_CREATED)
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
