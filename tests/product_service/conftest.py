import pytest

from src.product_service.utils.uow import ProductUOW


@pytest.fixture
def product_uow() -> ProductUOW:
    return ProductUOW()
