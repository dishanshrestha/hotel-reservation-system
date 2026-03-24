from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    usertype: str
    profile_photo_path: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserPublic


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
    phone: str | None = Field(default=None, max_length=255)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
