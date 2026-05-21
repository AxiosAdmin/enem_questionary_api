import uuid

import jwt
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.db_connection import async_session
from src.helpers.constraints import BYPASS_ROUTES
from src.models.models import Users
from src.utils.jwt_utils import decode_token


def should_bypass_auth(method: str, path: str) -> bool:
    normalized_path = path.rstrip("/") or "/"
    return method == "OPTIONS" or normalized_path in BYPASS_ROUTES


async def validate_token_user(user_id: str, db: AsyncSession) -> None:
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid token subject.") from exc

    result = await db.execute(select(Users.id).where(Users.id == user_uuid))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Token user no longer exists.")


async def jwt_validation(request: Request, call_next):
    if should_bypass_auth(request.method, request.url.path):
        return await call_next(request)

    authorization = request.headers.get("authorization")
    if not authorization:
        return JSONResponse(
            status_code=401,
            content={"detail": "Authorization header is required"},
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid authorization format. Use: Bearer <token>"},
        )

    try:
        decoded_token = decode_token(token, expected_type="access")
        user_id = decoded_token.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload.")

        async with async_session() as session:
            await validate_token_user(user_id, session)

        request.state.user = decoded_token
        request.state.user_id = user_id

    except jwt.ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"detail": "Token expired"})
    except (jwt.InvalidTokenError, HTTPException) as exc:
        status_code = getattr(exc, "status_code", 401)
        detail = getattr(exc, "detail", "Invalid token")
        return JSONResponse(status_code=status_code, content={"detail": detail})

    return await call_next(request)
