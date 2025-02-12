from pydantic import BaseModel, EmailStr, field_validator
from app.wallet.schemas import WalletsListResponse
from typing import Annotated
from annotated_types import MinLen
import re


class UserCreateRequest(BaseModel):

    username: Annotated[str, MinLen(3)]
    email: EmailStr
    password: Annotated[str, MinLen(3)]
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def check_password_match(cls, confirm_password, values):
        password = values.get("password")
        if password is not None and confirm_password != password:
            raise ValueError("Пароли не совпадают")
        return confirm_password

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if not re.search(r"^\\d+$", value):
            raise ValueError("Пароль должен содержать только цифры")
        if len(value) < 3:
            raise ValueError("Слишком короткий. Минимум 3 цифры")
        return value


class UserResponse(BaseModel):

    user_id: int
    username: str
    email: EmailStr
    wallets: WalletsListResponse
