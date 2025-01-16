from pydantic import BaseModel, model_validator


class MetaFieldScheme(BaseModel):
    id: int
    name: str
    data_type: str
    possible_values: list[str] | None
    coefficients: list[float] | None
    constant_coefficient: float = 1.0


class MetaFieldSchemeRequest(BaseModel):
    name: str
    data_type: str
    possible_values: list[str] | None
    coefficients: list[float] | None
    constant_coefficient: float = 1.0

    @model_validator(mode="after")
    def check_values_coefficients(self) -> "MetaFieldSchemeRequest":
        if self.possible_values is None and self.coefficients is not None:
            raise ValueError("possible_values is None and coefficients must be None")

        if self.coefficients is None and self.possible_values is not None:
            raise ValueError("coefficients is None and possible_values must be None")

        if (
            self.coefficients is None
            and self.possible_values is None
            and self.constant_coefficient is None
        ):
            raise ValueError(
                "coefficients or possible_values or constant_coefficient must not be None"
            )

        if (
            self.possible_values is not None
            and self.coefficients is not None
            and len(self.coefficients) != len(self.possible_values)
        ):
            raise ValueError(
                "length of coefficients and possible_values must match or both values is None"
            )

        return self
