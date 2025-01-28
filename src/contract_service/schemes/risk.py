from pydantic import BaseModel


class RiskScheme(BaseModel):
    id: int
    name: str
    rate: float
