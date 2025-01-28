from src.core.uow import UnitOfWork
from src.agent_service.repositories.agent_agreements import AgentAgreementsRepository
from src.agent_service.repositories.agent import AgentRepository
from src.agent_service.repositories.ikp import IkpRepository
from src.agent_service.repositories.face import FaceRepository


class AgentUOW(UnitOfWork):
    async def __aenter__(self) -> None:
        await super().__aenter__()

        self.agents = AgentRepository(self.session)
        self.agent_agreements = AgentAgreementsRepository(self.session)
        self.ikps = IkpRepository(self.session)
        self.faces = FaceRepository(self.session)
