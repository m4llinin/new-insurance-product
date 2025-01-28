from sqlalchemy.orm import Mapped

from src.core.dependencies import (
    int_pk,
    str_not_null,
)
from src.core.database.base import Base
from src.product_service.schemes.lob import LobScheme


class Lob(Base, scheme=LobScheme):
    __tablename__ = "lobs"

    id: Mapped[int_pk]
    name: Mapped[str_not_null]
