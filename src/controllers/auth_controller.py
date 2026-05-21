from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.auth_schema import (
    CreateUserRequest,
    ForgotPasswordRequest,
    LoginRequest,
)
from src.services.auth_service import AuthService


class AuthController:
    @staticmethod
    async def create_user(request: CreateUserRequest, db: AsyncSession):
        return await AuthService.create_user(request, db)

    @staticmethod
    async def login(request: LoginRequest, db: AsyncSession):
        return await AuthService.login(request, db)

    @staticmethod
    async def forgot_password(request: ForgotPasswordRequest, db: AsyncSession):
        return await AuthService.forgot_password(request, db)
