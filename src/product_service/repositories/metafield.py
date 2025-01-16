from src.core.database.base import SqlAlchemyRepository
from src.product_service.models import MetaField


class MetaFieldRepository(SqlAlchemyRepository, model=MetaField):
    pass
