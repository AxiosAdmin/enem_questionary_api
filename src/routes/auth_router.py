from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.db_connection import get_db
from src.controllers.auth_controller import AuthController
from src.schemas.auth_schema import (
    CreateUserRequest,
    CreateUserResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    LoginResponse,
)

auth_router = APIRouter()


@auth_router.post(
    "/register",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: CreateUserRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthController.create_user(request, db)


@auth_router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthController.login(request, db)


@auth_router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthController.forgot_password(request, db)
