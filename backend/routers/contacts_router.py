from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas.contacts import ContactRequest

router = APIRouter(prefix="/api", tags=["contacts"])


@router.post("/contact", status_code=status.HTTP_201_CREATED)
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
