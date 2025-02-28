from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.agent_service.models import Ikp
from src.agent_service.repositories.ikp import IkpRepository


class TestIkpRepository:
    async def test_insert_ikp_repository(
        self,
        mock_async_session: AsyncMock,
        ikp_repository: IkpRepository,
        ikp_data: dict[str, str | int],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(scalar_one=lambda: 1)

        result = await ikp_repository.insert(data=ikp_data)
        assert result == 1

    async def test_get_one_ikp_repository_found(
        self,
        mock_async_session: AsyncMock,
        ikp_repository: IkpRepository,
        ikp_data: dict[str, str | int],
        returning_ikp_data: dict[str, str | int],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Ikp(**returning_ikp_data)
        )

        result = await ikp_repository.get_one(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == ikp_data

    async def test_get_one_ikp_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        ikp_repository: IkpRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await ikp_repository.get_one(
            filters={
                "id": 999,
            },
        )

        assert result is None

    async def test_get_all_ikp_repository_found(
        self,
        mock_async_session: AsyncMock,
        ikp_repository: IkpRepository,
        returning_ikp_data_list: list[dict[str, str | int]],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            all=lambda: [(Ikp(**data),) for data in returning_ikp_data_list]
        )

        result = await ikp_repository.get_all({})

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    async def test_get_all_ikp_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        ikp_repository: IkpRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(all=lambda: [])

        result = await ikp_repository.get_all({})

        assert len(result) == 0

    async def test_update_ikp_repository_found(
        self,
        mock_async_session: AsyncMock,
        ikp_repository: IkpRepository,
        ikp_data: dict[str, str | int],
        returning_ikp_data: dict[str, str | int],
    ) -> None:
        ikp_data.update({"name": "VOKZAL"})
        returning_ikp_data.update({"name": "VOKZAL"})

        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Ikp(**returning_ikp_data)
        )

        result = await ikp_repository.update(
            filters={
                "id": 1,
            },
            data={
                "name": "VOKZAL",
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == ikp_data

    async def test_update_ikp_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        ikp_repository: IkpRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None,
        )

        result = await ikp_repository.update(
            filters={
                "id": 999,
            },
            data={
                "name": "VOKZAL",
            },
        )

        assert result is None

    async def test_delete_ikp_repository_found(
        self,
        mock_async_session: AsyncMock,
        ikp_repository: IkpRepository,
        ikp_data: dict[str, str | int],
        returning_ikp_data: dict[str, str | int],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Ikp(**returning_ikp_data)
        )

        result = await ikp_repository.delete(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == ikp_data

    async def test_delete_ikp_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        ikp_repository: IkpRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await ikp_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is None
