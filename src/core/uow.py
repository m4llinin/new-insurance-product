from abc import ABC, abstractmethod

from src.core.database.connection import DBConnection


class UnitOfWorkABC(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(UnitOfWorkABC):
    def __init__(self):
        self.async_sessionmaker = DBConnection.get_instance().async_sessionmaker

    async def __aenter__(self):
        self.session = self.async_sessionmaker()

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
