from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
from database import get_db
from services.image_service import _as_public_image_path

router = APIRouter(prefix="/api", tags=["gallery"])


@router.get("/gallery")
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


@router.get("/hotel_gallary")
def list_gallery_legacy(db: Session = Depends(get_db)):
    return list_gallery(db=db)
