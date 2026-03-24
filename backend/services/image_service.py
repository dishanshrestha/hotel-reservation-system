from __future__ import annotations

import datetime as dt
import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"


def _as_public_image_path(value: str | None) -> str | None:
    if not value:
        return value
    stripped = value.strip()
    if stripped.startswith(("http://", "https://", "/")):
        return stripped
    return f"/media/{stripped.lstrip('/')}"


def _save_upload(file: UploadFile, sub_dir: str) -> str:
    folder = MEDIA_DIR / sub_dir
    folder.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename or "").suffix
    filename = f"{int(dt.datetime.utcnow().timestamp())}_{uuid.uuid4().hex[:8]}{extension}"
    destination = folder / filename

    with destination.open("wb") as output:
        shutil.copyfileobj(file.file, output)

    return f"{sub_dir}/{filename}"
