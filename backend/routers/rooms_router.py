from __future__ import annotations

import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import models
from database import get_db
from services.booking_service import _find_next_available_slots, _room_exists
from services.room_service import (
    _as_bool_flag,
    _filter_rooms,
    _recommend_rooms_for_stay,
    _serialize_room,
)

router = APIRouter(prefix="/api", tags=["rooms"])


@router.get("/rooms")
def list_rooms(
    price_range: str | None = Query(default=None),
    room_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    rooms = _filter_rooms(db, price_range, room_type)
    return {"count": len(rooms), "rooms": rooms}


@router.get("/our_rooms")
def our_rooms(
    price_range: str | None = Query(default=None),
    room_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return list_rooms(price_range=price_range, room_type=room_type, db=db)


@router.get("/search-rooms")
def search_rooms(
    price_range: str | None = Query(default=None),
    room_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return list_rooms(price_range=price_range, room_type=room_type, db=db)


@router.get("/rooms/{room_id}")
def room_details(room_id: int, db: Session = Depends(get_db)):
    room = db.get(models.Room, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return _serialize_room(db, room, include_ratings=True)


@router.get("/room_details/{room_id}")
def legacy_room_details(room_id: int, db: Session = Depends(get_db)):
    return room_details(room_id=room_id, db=db)


@router.get("/recommendations/rooms")
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


@router.get("/rooms/{room_id}/availability-suggestions")
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
