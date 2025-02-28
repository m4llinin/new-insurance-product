import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.product_service.repositories.lob import LobRepository
from src.product_service.repositories.metafield import MetaFieldRepository
from src.product_service.repositories.product import ProductRepository


@pytest.fixture
def lob_repository(mock_async_session: AsyncSession) -> LobRepository:
    return LobRepository(session=mock_async_session)


@pytest.fixture
def metafield_repository(mock_async_session: AsyncSession) -> MetaFieldRepository:
    return MetaFieldRepository(session=mock_async_session)


@pytest.fixture
def product_repository(mock_async_session: AsyncSession) -> ProductRepository:
    return ProductRepository(session=mock_async_session)


@pytest.fixture
def lob_data() -> dict[str, str]:
    return {
        "name": "VASKA",
    }


@pytest.fixture
def returning_lob_data() -> dict[str, str]:
    return {
        "id": 1,
        "name": "VASKA",
    }


@pytest.fixture
def returning_lob_data_list() -> list[dict[str, str | int]]:
    return [
        {
            "id": 1,
            "name": "VASKA",
        },
        {
            "id": 2,
            "name": "PETROGA",
        },
    ]


@pytest.fixture
def metafield_data() -> dict[str, str]:
    return {
        "name": "VASKA",
        "data_type": "string",
        "constant_coefficient": 23.24,
        "coefficients": None,
        "possible_values": None,
    }


@pytest.fixture
def returning_metafield_data() -> dict[str, str]:
    return {
        "id": 1,
        "name": "VASKA",
        "data_type": "string",
        "constant_coefficient": 23.24,
    }


@pytest.fixture
def returning_metafield_data_list() -> list[dict[str, str | int]]:
    return [
        {
            "id": 1,
            "name": "VASKA",
            "data_type": "string",
            "constant_coefficient": 23.24,
        },
        {
            "id": 2,
            "name": "VASKA",
            "data_type": "string",
            "constant_coefficient": 20.67,
        },
    ]


@pytest.fixture
def product_data() -> dict[str, str]:
    return {
        "name": "VASKA",
        "lob_id": 1,
        "basic_rate": 1.2,
        "meta_fields": [1, 2],
    }


@pytest.fixture
def returning_product_data() -> dict[str, str]:
    return {
        "id": 1,
        "name": "VASKA",
        "lob_id": 1,
        "basic_rate": 1.2,
        "meta_fields": [1, 2],
    }


@pytest.fixture
def returning_product_data_list() -> list[dict[str, str | int]]:
    return [
        {
            "id": 1,
            "name": "VASKA",
            "lob_id": 1,
            "basic_rate": 1.2,
            "meta_fields": [1, 2],
        },
        {
            "id": 2,
            "name": "VASKA",
            "lob_id": 1,
            "basic_rate": 1.2,
            "meta_fields": [1, 2],
        },
    ]
