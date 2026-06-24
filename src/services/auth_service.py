from urllib.parse import urlencode

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.configs import settings
from src.models.models import Subscriptions, Users
from src.schemas.auth_schema import (
    CreateUserRequest,
    ForgotPasswordRequest,
    LoginRequest,
)
from src.utils.email_utils import send_password_reset_email
from src.utils.fernet_utils import FernetUtils
from src.utils.hash_utils import hash_lookup_value, normalize_nickname
from src.utils.jwt_utils import create_access_token, create_password_reset_token
from src.utils.password_utils import hash_password, verify_password


class AuthService:
    @staticmethod
    async def create_user(request: CreateUserRequest, db: AsyncSession) -> dict:
        email_hash = hash_lookup_value(request.email)
        cpf_hash = hash_lookup_value(request.cpf)
        nickname_hash = hash_lookup_value(normalize_nickname(request.nickname))

        existing_user = await db.execute(
            select(Users).where(
                (Users.email_hash == email_hash)
                | (Users.cpf_hash == cpf_hash)
                | (Users.nickname_hash == nickname_hash)
            )
        )
        matched_user = existing_user.scalar_one_or_none()
        if matched_user is not None:
            if matched_user.email_hash == email_hash:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered.",
                )
            if matched_user.cpf_hash == cpf_hash:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="CPF already registered.",
                )
            if matched_user.nickname_hash == nickname_hash:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Nickname already registered.",
                )

        user = Users(
            name=FernetUtils.encrypt(request.name),
            email=FernetUtils.encrypt(request.email),
            cpf=FernetUtils.encrypt(request.cpf),
            nickname=FernetUtils.encrypt(request.nickname),
            email_hash=email_hash,
            cpf_hash=cpf_hash,
            nickname_hash=nickname_hash,
            password=hash_password(request.password),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return {"data": await AuthService._serialize_user(user, db)}

    @staticmethod
    async def login(request: LoginRequest, db: AsyncSession) -> dict:
        email_hash = hash_lookup_value(request.email)
        result = await db.execute(select(Users).where(Users.email_hash == email_hash))
        user = result.scalar_one_or_none()

        if user is None or not verify_password(request.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        return {
            "access_token": create_access_token(str(user.id), user.global_role),
            "token_type": "bearer",
            "data": await AuthService._serialize_user(user, db),
        }

    @staticmethod
    async def forgot_password(request: ForgotPasswordRequest, db: AsyncSession) -> dict:
        email_hash = hash_lookup_value(request.email)
        result = await db.execute(select(Users).where(Users.email_hash == email_hash))
        user = result.scalar_one_or_none()

        if user is None:
            return {
                "message": (
                    "If the email exists, password reset instructions were generated."
                )
            }

        reset_token = create_password_reset_token(str(user.id), user.email_hash)
        reset_url = AuthService._build_password_reset_url(reset_token)
        send_password_reset_email(request.email, reset_url)

        response = {
            "message": "If the email exists, password reset instructions were generated."
        }
        if settings.PASSWORD_RESET_INCLUDE_TOKEN_IN_RESPONSE:
            response["reset_token"] = reset_token
            response["reset_url"] = reset_url

        return response

    @staticmethod
    async def _serialize_user(user: Users, db: AsyncSession) -> dict:
        is_first_purchase_eligible = await AuthService._is_first_purchase_eligible(
            user.id, db
        )
        return {
            "id": user.id,
            "name": FernetUtils.decrypt(user.name),
            "email": FernetUtils.decrypt(user.email),
            "nickname": FernetUtils.decrypt(user.nickname),
            "cpf": FernetUtils.decrypt(user.cpf),
            "global_role": user.global_role,
            "first_purchase_coupon_eligible": is_first_purchase_eligible,
        }

    @staticmethod
    async def _is_first_purchase_eligible(
        user_id,
        db: AsyncSession,
    ) -> bool:
        result = await db.execute(
            select(Subscriptions.id)
            .where(
                Subscriptions.user_id == user_id,
                Subscriptions.status.in_(["active", "trialing", "canceled"]),
            )
            .limit(1)
        )
        return result.scalar_one_or_none() is None

    @staticmethod
    def _build_password_reset_url(reset_token: str) -> str:
        separator = "&" if "?" in settings.PASSWORD_RESET_URL else "?"
        return (
            f"{settings.PASSWORD_RESET_URL}{separator}"
            f"{urlencode({'token': reset_token})}"
        )
