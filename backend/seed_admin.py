from __future__ import annotations

import argparse

from sqlalchemy.orm import Session

import models
from auth import get_password_hash
from database import SessionLocal


def seed_admin(db: Session, name: str, email: str, password: str, phone: str | None) -> models.User:
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        existing.name = name
        existing.phone = phone
        existing.usertype = "admin"
        existing.password = get_password_hash(password)
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing

    user = models.User(
        name=name,
        email=email,
        phone=phone,
        usertype="admin",
        password=get_password_hash(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or update an admin account")
    parser.add_argument("--name", default="Admin")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--phone", default=None)
    args = parser.parse_args()

    db = SessionLocal()
    try:
        user = seed_admin(db, args.name, args.email, args.password, args.phone)
        print(f"Admin ready: id={user.id} email={user.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
