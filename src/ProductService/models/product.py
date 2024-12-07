from sqlalchemy import ForeignKey, ARRAY, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.core.dependencies import int_pk, str_not_null
from src.core.database.base import Base
from src.ProductService.schemes.products import ProductScheme


class Product(Base):
    __tablename__ = 'products'

    _scheme = ProductScheme

    id: Mapped[int_pk]
    name: Mapped[str_not_null]
    lob_id: Mapped[int] = mapped_column(ForeignKey('lobs.id'))
    basic_rate: Mapped[float] = mapped_column(default=1.0)
    meta_fields: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)
