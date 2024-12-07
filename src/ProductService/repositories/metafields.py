from src.core.database.base import SqlAlchemyRepository
from src.ProductService.models.metafield import MetaField


class MetaFieldRepository(SqlAlchemyRepository):
    model = MetaField
