from enum import Enum

from pydantic import BaseModel, EmailStr


class Role(Enum):
    ADMIN = "admin"
    USER = "user"


class AuthScheme(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    is_active: bool


class AuthSchemeRequest(BaseModel):
    email: EmailStr
    password: str


class AuthSchemeResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None


class AuthSchemeIdResponse(BaseModel):
    id: int
