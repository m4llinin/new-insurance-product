from sqlalchemy.orm import Mapped

from src.core.dependencies import int_pk, str_not_null
from src.core.database.base import Base
from src.ProductService.schemes.lobs import LobScheme


class Lob(Base):
    __tablename__ = 'lobs'

    _scheme = LobScheme

    id: Mapped[int_pk]
    name: Mapped[str_not_null]
