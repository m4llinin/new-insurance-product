from datetime import datetime
from enum import Enum
from pydantic import (
    BaseModel,
    model_validator,
    field_validator,
)


class ContractStatuses(Enum):
    DRAFT = "DRAFT"
    SIGNED = "SIGNED"
    TERMINATED = "TERMINATED"


class ContractBaseModel(BaseModel):
    date_create: datetime
    date_sign: datetime
    date_begin: datetime
    date_end: datetime

    @field_validator("date_begin", "date_sign", "date_end", "date_create")
    def remove_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class ContractScheme(ContractBaseModel):
    id: int
    product_id: int
    premium: float
    insurance_sum: float
    agent_id: int
    rate: float
    commission: float
    status: ContractStatuses
    policy_holder_id: int
    insured_personal_id: int
    owner_id: int
    policy_price: float
    risk_id: list[int]


class ContractAddScheme(ContractBaseModel):
    product_id: int
    premium: float
    insurance_sum: float
    policy_price: float
    status: ContractStatuses
    agent_id: int
    policy_holder_id: int
    insured_personal_id: int
    owner_id: int
    risk_id: list[int]


class ContractFiltersScheme(BaseModel):
    id: int | None = None
    date_create: datetime | None = None
    date_sign: datetime | None = None
    product_id: int | None = None
    date_begin: datetime | None = None
    date_end: datetime | None = None
    premium: float | None = None
    insurance_sum: float | None = None
    agent_id: int | None = None
    rate: float | None = None
    commission: float | None = None
    status: ContractStatuses | None = None
    policy_holder_id: int | None = None
    insured_personal_id: int | None = None
    owner_id: int | None = None

    @model_validator(mode="after")
    def check_dates(self) -> "ContractFiltersScheme":
        if (self.date_begin is None) + (self.date_end is None) == 1:
            raise ValueError(
                "Period must have range. Now, date begin or date end is none"
            )
        if (
            self.date_begin is not None
            and self.date_end is not None
            and self.date_end < self.date_begin
        ):
            raise ValueError("Date end must be bigger than date begin")
        return self


class ContractIdResponse(BaseModel):
    id: int


class PeriodScheme(BaseModel):
    date_begin: datetime
    date_end: datetime

    @field_validator("date_begin", "date_end")
    def remove_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class ProductScheme(BaseModel):
    id: int
    name: str


class ProductStatisticsScheme(BaseModel):
    id: int
    name: str
    all_commission: float
    all_premium: float


class OneContractSchemeResponse(BaseModel):
    id: int
    product: ProductScheme
    premium: float
    rate: float
    commission: float


class ContractStatisticsSchemeResponse(BaseModel):
    contracts: list[OneContractSchemeResponse]
    all_commission: float
    all_premium: float
    products: list[ProductStatisticsScheme]


class ProductCommissionPremium(BaseModel):
    commission: float = 0
    premium: float = 0


class MetaFieldScheme(BaseModel):
    id: int
    value: float | str


class CalculatePriceScheme(BaseModel):
    product_id: int
    count_days: int
    insurance_sum: float
    risk_id: list[int]
    meta_fields: list[MetaFieldScheme]


class CalculatePriceResponse(BaseModel):
    price: float
