from enum import Enum
from typing import Type
from pydantic import (
    BaseModel,
    EmailStr,
    field_serializer,
)


class Role(Enum):
    ADMIN = "admin"
    USER = "user"


class AuthScheme(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    role: Role
    is_active: bool

    @field_serializer("role")
    def serialize_role(self, role: Type[Role], _info) -> str:
        return role.value


class AuthSchemeRequest(BaseModel):
    email: EmailStr
    password: str


class AuthSchemeResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None


class AuthSchemeIdResponse(BaseModel):
    id: int
