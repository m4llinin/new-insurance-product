from src.core.uow import UnitOfWork

from src.ProductService.repositories.products import ProductRepository
from src.ProductService.repositories.metafields import MetaFieldRepository
from src.ProductService.repositories.lobs import LobRepository


class ProductUOW(UnitOfWork):
    async def __aenter__(self):
        self.session = self.async_sessionmaker()

        self.products = ProductRepository(self.session)
        self.meta_fields = MetaFieldRepository(self.session)
        self.lobs = LobRepository(self.session)
