from __future__ import annotations

import datetime as dt
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field, model_validator


class BookingCreateRequest(BaseModel):
    room_id: int
    start_date: dt.date
    end_date: dt.date
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=255)
    total_price: Decimal | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingCreateRequest":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class BookingCreateByRoomRequest(BaseModel):
    start_date: dt.date
    end_date: dt.date
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=255)
    total_price: Decimal | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingCreateByRoomRequest":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class CheckoutRequest(BaseModel):
    room_id: int
    start_date: dt.date
    end_date: dt.date
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    phone: str = Field(min_length=1, max_length=255)
    total_price: Decimal = Field(gt=0)

    @model_validator(mode="after")
    def validate_dates(self) -> "CheckoutRequest":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class BookingStatusRequest(BaseModel):
    status: str
