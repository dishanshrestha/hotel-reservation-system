from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class ContactRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    phone: str = Field(min_length=1, max_length=255)
    message: str = Field(min_length=1)
