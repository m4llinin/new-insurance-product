from src.core.utils.uow import UnitOfWork

from src.product_service.repositories.product import ProductRepository
from src.product_service.repositories.metafield import MetaFieldRepository
from src.product_service.repositories.lob import LobRepository


class ProductUOW(UnitOfWork):
    async def __aenter__(self) -> None:
        await super().__aenter__()

        self.products = ProductRepository(self.session)
        self.meta_fields = MetaFieldRepository(self.session)
        self.lobs = LobRepository(self.session)
