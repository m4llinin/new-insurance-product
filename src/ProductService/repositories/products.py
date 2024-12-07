from src.core.database.base import SqlAlchemyRepository
from src.ProductService.models.product import Product


class ProductRepository(SqlAlchemyRepository):
    model = Product
