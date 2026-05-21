from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from src.configs.configs import settings


def create_access_token(user_id: str, role: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRATION_MINUTES
    )
    payload: dict[str, Any] = {
        "sub": user_id,
        "role": role,
        "type": "access",
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)


def create_password_reset_token(user_id: str, email_hash: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.PASSWORD_RESET_TOKEN_EXPIRATION_MINUTES
    )
    payload: dict[str, Any] = {
        "sub": user_id,
        "email_hash": email_hash,
        "type": "password_reset",
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str, expected_type: str | None = None) -> dict[str, Any]:
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    token_type = payload.get("type")
    if expected_type is not None and token_type != expected_type:
        raise jwt.InvalidTokenError("Invalid token type.")

    return payload
