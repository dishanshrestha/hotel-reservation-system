from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas.ratings import RatingRequest

router = APIRouter(prefix="/api", tags=["ratings"])


@router.post("/ratings/{room_id}", status_code=status.HTTP_201_CREATED)
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


@router.post("/save-rating/{room_id}", status_code=status.HTTP_201_CREATED)
def save_rating_legacy(room_id: int, payload: RatingRequest, db: Session = Depends(get_db)):
    return save_rating(room_id=room_id, payload=payload, db=db)
