from sqlalchemy import ARRAY, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.core.dependencies import int_pk, str_not_null
from src.core.database.base import Base
from src.ProductService.schemes.metafields import MetaFieldScheme


class MetaField(Base):
    __tablename__ = 'metafields'

    _scheme = MetaFieldScheme

    id: Mapped[int_pk]
    name: Mapped[str_not_null]
    data_type: Mapped[str_not_null]
    possible_values: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    coefficients: Mapped[list[float]] = mapped_column(ARRAY(Float), nullable=True)
    constant_coefficient: Mapped[float] = mapped_column(default=1.0)
