from datetime import datetime
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.agent_service.models import Face
from src.agent_service.repositories.face import FaceRepository


class TestFaceRepository:
    async def test_insert_face_repository(
        self,
        mock_async_session: AsyncMock,
        face_repository: FaceRepository,
        face_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(scalar_one=lambda: 1)

        result = await face_repository.insert(data=face_data)
        assert result == 1

    async def test_get_one_face_repository_found(
        self,
        mock_async_session: AsyncMock,
        face_repository: FaceRepository,
        face_data: dict[str, str | int | datetime],
        returning_face_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Face(**returning_face_data)
        )

        result = await face_repository.get_one(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == face_data

    async def test_get_one_face_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        face_repository: FaceRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await face_repository.get_one(
            filters={
                "id": 999,
            },
        )

        assert result is None

    async def test_get_all_face_repository_found(
        self,
        mock_async_session: AsyncMock,
        face_repository: FaceRepository,
        returning_face_data_list: list[dict[str, str | int | datetime]],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            all=lambda: [(Face(**data),) for data in returning_face_data_list]
        )

        result = await face_repository.get_all({})

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    async def test_get_all_face_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        face_repository: FaceRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(all=lambda: [])

        result = await face_repository.get_all({})

        assert len(result) == 0

    async def test_update_face_repository_found(
        self,
        mock_async_session: AsyncMock,
        face_repository: FaceRepository,
        face_data: dict[str, str | int | datetime],
        returning_face_data: dict[str, str | int | datetime],
    ) -> None:
        face_data.update({"first_name": "ALEX"})
        returning_face_data.update({"first_name": "ALEX"})

        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Face(**returning_face_data)
        )

        result = await face_repository.update(
            filters={
                "id": 1,
            },
            data={
                "first_name": "ALEX",
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == face_data

    async def test_update_face_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        face_repository: FaceRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None,
        )

        result = await face_repository.update(
            filters={
                "id": 999,
            },
            data={
                "first_name": "ALEX",
            },
        )

        assert result is None

    async def test_delete_face_repository_found(
        self,
        mock_async_session: AsyncMock,
        face_repository: FaceRepository,
        face_data: dict[str, str | int | datetime],
        returning_face_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Face(**returning_face_data)
        )

        result = await face_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == face_data

    async def test_delete_face_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        face_repository: FaceRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await face_repository.delete(
            filters={
                "id": 1
            },
        )

        assert result is None
