from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
from services.image_service import _as_public_image_path


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


def _recommend_rooms_for_stay(
    db: Session,
    rooms: list[dict[str, Any]],
    start_date: "dt.date | None",
    end_date: "dt.date | None",
    room_type: str | None,
    max_budget: float | None,
    wifi_required: bool | None,
    top_k: int,
) -> list[dict[str, Any]]:
    import datetime as dt
    import heapq

    from services.booking_service import _booking_overlaps

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
