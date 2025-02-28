from src.product_service.utils.uow import ProductUOW
from src.product_service.repositories.lob import LobRepository
from src.product_service.repositories.metafield import MetaFieldRepository
from src.product_service.repositories.product import ProductRepository


class TestProductUOW:
    async def test_product_uow_initialization(
        self,
        product_uow: ProductUOW,
    ) -> None:
        async with product_uow:
            assert isinstance(product_uow.products, ProductRepository)
            assert isinstance(product_uow.meta_fields, MetaFieldRepository)
            assert isinstance(product_uow.lobs, LobRepository)

    async def test_product_uow_context_manager(
        self,
        product_uow: ProductUOW,
    ) -> None:
        assert not hasattr(product_uow, "products")
        assert not hasattr(product_uow, "meta_fields")
        assert not hasattr(product_uow, "lobs")

        async with product_uow:
            assert hasattr(product_uow, "products")
            assert hasattr(product_uow, "meta_fields")
            assert hasattr(product_uow, "lobs")
