from datetime import datetime

from sqlalchemy import Enum
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.agent_service.schemes.face import (
    FaceScheme,
    TypeFace,
)
from src.core.database.base import Base
from src.core.dependencies import (
    int_pk,
    str_not_null,
)


class Face(Base, scheme=FaceScheme):
    __tablename__ = "faces"

    id: Mapped[int_pk]
    type: Mapped[str] = mapped_column(Enum(TypeFace), default=TypeFace.natural)
    first_name: Mapped[str_not_null]
    second_name: Mapped[str_not_null]
    last_name: Mapped[str_not_null]
    date_of_birth: Mapped[datetime] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=True)
    inn: Mapped[int]
