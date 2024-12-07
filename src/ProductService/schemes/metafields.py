from pydantic import BaseModel


class MetaFieldScheme(BaseModel):
    id: int
    name: str
    data_type: str
    possible_values: list[str] | None
    coefficients: list[float] | None
    constant_coefficient: float


class MetaFieldSchemeRequest(BaseModel):
    name: str
    data_type: str
    possible_values: list[str] | None
    coefficients: list[float] | None
    constant_coefficient: float
