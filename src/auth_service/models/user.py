from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base
from src.core.dependencies import (
    int_pk,
    str_not_null,
)

from src.auth_service.schemes.auth import AuthScheme
from src.auth_service.schemes.auth import Role


class User(Base, scheme=AuthScheme):
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str_not_null]
    hashed_password: Mapped[str_not_null]
    role: Mapped[str] = mapped_column(Enum(Role), default=Role.USER, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)
