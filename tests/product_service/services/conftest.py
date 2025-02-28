from unittest.mock import AsyncMock

import pytest

from src.product_service.utils.uow import ProductUOW
from src.product_service.services.product import ProductService
from src.product_service.services.metafield import MetaFieldService
from src.product_service.services.lob import LobService


@pytest.fixture
def mock_product_uow() -> AsyncMock:
    uow = AsyncMock(spec=ProductUOW)
    uow.products = AsyncMock()
    uow.meta_fields = AsyncMock()
    uow.lobs = AsyncMock()
    return uow


@pytest.fixture
def product_service(mock_product_uow: AsyncMock) -> ProductService:
    return ProductService(uow=mock_product_uow)


@pytest.fixture
def metafield_service(mock_product_uow: AsyncMock) -> MetaFieldService:
    return MetaFieldService(uow=mock_product_uow)


@pytest.fixture
def lob_service(mock_product_uow: AsyncMock) -> LobService:
    return LobService(uow=mock_product_uow)
