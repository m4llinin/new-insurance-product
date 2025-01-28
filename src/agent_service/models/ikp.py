from sqlalchemy.orm import Mapped

from src.agent_service.schemes.ikp import IkpScheme
from src.core.database.base import Base
from src.core.dependencies import (
    int_pk,
    str_not_null,
)


class Ikp(Base, scheme=IkpScheme):
    __tablename__ = "ikps"

    id: Mapped[int_pk]
    name: Mapped[str_not_null]
