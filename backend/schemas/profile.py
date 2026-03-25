from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, model_validator


class ProfileUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=255)


class PasswordUpdateRequest(BaseModel):
    current_password: str
    password: str = Field(min_length=8, max_length=255)
    password_confirmation: str

    @model_validator(mode="after")
    def validate_password_confirmation(self) -> "PasswordUpdateRequest":
        if self.password != self.password_confirmation:
            raise ValueError("Password confirmation does not match")
        return self
