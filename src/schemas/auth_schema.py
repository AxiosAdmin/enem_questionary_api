import re
import uuid

from pydantic import BaseModel, field_validator

from src.utils.hash_utils import normalize_cpf, normalize_email, normalize_nickname


class CreateUserRequest(BaseModel):
    name: str
    email: str
    cpf: str
    nickname: str
    password: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Name must have at least 3 characters.")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized_value = normalize_email(value)
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized_value):
            raise ValueError("Invalid email.")
        return normalized_value

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        normalized_value = normalize_cpf(value)
        if len(normalized_value) != 11:
            raise ValueError("CPF must have 11 digits.")
        return normalized_value

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, value: str) -> str:
        trimmed_value = value.strip()
        if len(normalize_nickname(trimmed_value)) < 3:
            raise ValueError("Nickname must have at least 3 characters.")
        return trimmed_value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters.")
        return value


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized_value = normalize_email(value)
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized_value):
            raise ValueError("Invalid email.")
        return normalized_value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value:
            raise ValueError("Password is required.")
        return value


class ForgotPasswordRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized_value = normalize_email(value)
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized_value):
            raise ValueError("Invalid email.")
        return normalized_value


class AuthUserResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    nickname: str
    cpf: str
    global_role: str
    first_purchase_coupon_eligible: bool


class CreateUserResponse(BaseModel):
    data: AuthUserResponse


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    data: AuthUserResponse


class ForgotPasswordResponse(BaseModel):
    message: str
    reset_token: str | None = None
    reset_url: str | None = None
