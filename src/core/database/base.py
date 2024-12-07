from abc import ABC, abstractmethod
from typing import Any, Callable

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped
from src.core.dependencies import created_at, updated_at


class Base(DeclarativeBase):
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    _scheme: Callable = None

    def to_dict(self) -> dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def to_scheme(self):
        return self._scheme(**self.to_dict())

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {' '.join([f'{k}={v}' for k, v in self.to_dict().items()])}>"


class RepositoryABC(ABC):
    @abstractmethod
    async def get_one(self, data: dict) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, data: dict) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def insert(self, data: dict) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def update(self, filters: dict, data: dict) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, data: dict) -> Any:
        raise NotImplementedError


class SqlAlchemyRepository(RepositoryABC):
    model = None

    def __init__(self, session: AsyncSession):
        self._session = session

    async def insert(self, data: dict[str, Any]) -> Any:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def get_one(self, filters: dict[str, Any]) -> Any | None:
        stmt = select(self.model).filter_by(**filters)
        res = await self._session.execute(stmt)
        res = res.scalar_one_or_none()

        if res is not None:
            return res.to_scheme()

    async def get_all(self, filters: dict[str, Any]) -> Any:
        stmt = select(self.model).filter_by(**filters)
        res = await self._session.execute(stmt)
        return [r[0].to_scheme() for r in res.all()]

    async def update(self, filters: dict[str, Any], data: dict[str, Any]) -> Any:
        stmt = update(self.model).values(**data).filter_by(**filters).returning(self.model)
        res = await self._session.execute(stmt)
        return res.scalar_one().to_scheme()

    async def delete(self, filters: dict[str, Any]) -> Any:
        stmt = delete(self.model).filter_by(**filters).returning(self.model)
        res = await self._session.execute(stmt)
        return res.scalar_one().to_scheme()
