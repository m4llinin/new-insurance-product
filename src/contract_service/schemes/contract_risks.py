from pydantic import BaseModel


class ContractRiskScheme(BaseModel):
    id: int
    contract_id: int
    risk_id: list[int]
    premium: float
    insurance_sum: float
