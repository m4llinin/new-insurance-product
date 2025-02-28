from src.agent_service.utils.uow import AgentUOW
from src.agent_service.repositories.agent import AgentRepository
from src.agent_service.repositories.agent_agreements import AgentAgreementsRepository
from src.agent_service.repositories.ikp import IkpRepository
from src.agent_service.repositories.face import FaceRepository


class TestAgentUOW:
    async def test_agent_uow_initialization(
        self,
        agent_uow: AgentUOW,
    ) -> None:
        async with agent_uow:
            assert isinstance(agent_uow.agents, AgentRepository)
            assert isinstance(agent_uow.agent_agreements, AgentAgreementsRepository)
            assert isinstance(agent_uow.ikps, IkpRepository)
            assert isinstance(agent_uow.faces, FaceRepository)

    async def test_agent_uow_context_manager(
        self,
        agent_uow: AgentUOW,
    ) -> None:
        assert not hasattr(agent_uow, "agents")
        assert not hasattr(agent_uow, "agent_agreements")
        assert not hasattr(agent_uow, "ikps")
        assert not hasattr(agent_uow, "faces")

        async with agent_uow:
            assert hasattr(agent_uow, "agents")
            assert hasattr(agent_uow, "agent_agreements")
            assert hasattr(agent_uow, "ikps")
            assert hasattr(agent_uow, "faces")
