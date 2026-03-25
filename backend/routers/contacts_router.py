from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas.contacts import ContactRequest
from services.booking_service import _send_contact_confirmation_email

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

    email_sent, email_msg = _send_contact_confirmation_email(
        {"name": payload.name, "email": payload.email, "message": payload.message},
        db=db,
    )

    return {
        "message": "Message sent successfully",
        "contact_id": contact.id,
        "email_confirmation_sent": email_sent,
        "email_confirmation_message": email_msg,
    }
