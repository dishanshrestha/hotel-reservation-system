from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class RatingRequest(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    comment: str = Field(min_length=1, max_length=255)
    rating: int = Field(ge=1, le=5)
