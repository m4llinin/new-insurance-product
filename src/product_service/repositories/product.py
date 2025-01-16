from src.core.database.base import SqlAlchemyRepository
from src.product_service.models import Product


class ProductRepository(SqlAlchemyRepository, model=Product):
    pass
