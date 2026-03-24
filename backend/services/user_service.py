from __future__ import annotations

from typing import Any

import models


def _serialize_user(user: models.User) -> dict[str, Any]:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "usertype": user.usertype,
        "profile_photo_path": user.profile_photo_path,
    }
