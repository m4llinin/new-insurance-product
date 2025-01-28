from pydantic import BaseModel


class AgentAgreementsScheme(BaseModel):
    id: int
    agent_id: int
    lob_id: int
    rate: float
