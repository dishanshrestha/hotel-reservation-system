from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from auth import get_current_user, get_password_hash, verify_password
from database import get_db
from schemas.auth import UserPublic
from schemas.profile import PasswordUpdateRequest, ProfileUpdateRequest
from services.user_service import _serialize_user

router = APIRouter(prefix="/api", tags=["profile"])


@router.get("/profile", response_model=UserPublic)
def get_profile(current_user: models.User = Depends(get_current_user)):
    return _serialize_user(current_user)


@router.put("/profile", response_model=UserPublic)
def update_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if payload.email and payload.email != current_user.email:
        exists = db.query(models.User).filter(models.User.email == payload.email).first()
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        current_user.email = payload.email

    if payload.name is not None:
        current_user.name = payload.name
    if payload.phone is not None:
        current_user.phone = payload.phone

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return _serialize_user(current_user)


@router.put("/profile/password")
def update_profile_password(
    payload: PasswordUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not verify_password(payload.current_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

    current_user.password = get_password_hash(payload.password)
    db.add(current_user)
    db.commit()
    return {"message": "Password updated successfully"}


@router.put("/settings", response_model=UserPublic)
def update_settings(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return update_profile(payload=payload, db=db, current_user=current_user)
