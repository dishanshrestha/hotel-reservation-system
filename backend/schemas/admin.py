from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class AdminUserUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=255)
    usertype: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=255)
