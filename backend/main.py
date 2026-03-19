"""Compatibility ASGI entrypoint.

Allows running the backend with either:
- uvicorn app:app
- uvicorn main:app
"""

from app import app
