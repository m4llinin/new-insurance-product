from src.auth_service.utils.uow import AuthUOW
from src.auth_service.repostories.user import UserRepository


class TestAuthUOW:
    async def test_agent_uow_initialization(
        self,
        auth_uow: AuthUOW,
    ) -> None:
        async with auth_uow:
            assert isinstance(auth_uow.users, UserRepository)

    async def test_agent_uow_context_manager(
        self,
        auth_uow: AuthUOW,
    ) -> None:
        assert not hasattr(auth_uow, "users")

        async with auth_uow:
            assert hasattr(auth_uow, "users")
