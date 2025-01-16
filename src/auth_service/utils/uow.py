from src.core.uow import UnitOfWork

from src.auth_service.repostories.user import UserRepository


class AuthUOW(UnitOfWork):
    async def __aenter__(self) -> None:
        await super().__aenter__()

        self.users = UserRepository(self.session)
