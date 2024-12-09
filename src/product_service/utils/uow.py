from src.core.uow import UnitOfWork

from src.product_service.repositories.product import ProductRepository
from src.product_service.repositories.metafield import MetaFieldRepository
from src.product_service.repositories.lob import LobRepository


class ProductUOW(UnitOfWork):
    async def __aenter__(self):
        self.session = self.async_sessionmaker()

        self.products = ProductRepository(self.session)
        self.meta_fields = MetaFieldRepository(self.session)
        self.lobs = LobRepository(self.session)
