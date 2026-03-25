from __future__ import annotations

from sqlalchemy.orm import Session

import models

SMTP_KEYS = ("smtp_host", "smtp_port", "smtp_username", "smtp_password", "smtp_sender", "smtp_use_tls")


def get_setting(db: Session, key: str) -> str | None:
    row = db.query(models.SiteSetting).filter(models.SiteSetting.key == key).first()
    return row.value if row else None


def set_setting(db: Session, key: str, value: str | None) -> None:
    row = db.query(models.SiteSetting).filter(models.SiteSetting.key == key).first()
    if row:
        row.value = value
    else:
        row = models.SiteSetting(key=key, value=value)
        db.add(row)


def get_smtp_settings(db: Session) -> dict[str, str | None]:
    return {k: get_setting(db, k) for k in SMTP_KEYS}


def save_smtp_settings(db: Session, settings: dict[str, str | None]) -> None:
    for k in SMTP_KEYS:
        if k in settings:
            set_setting(db, k, settings[k])
    db.commit()
