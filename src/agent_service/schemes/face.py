from typing import Self
from pydantic import (
    BaseModel,
    model_validator,
)
from enum import Enum
from datetime import datetime


class TypeFace(Enum):
    natural = "natural"
    legal = "legal"



class FaceScheme(BaseModel):
    id: int
    type: TypeFace
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime | None = None
    name: str | None
    inn: int

    @model_validator(mode="after")
    def check_type_and_fields(self) -> Self:
        if (
            self.type == TypeFace.legal
            and (
                (self.first_name is None)
                + (self.second_name is None)
                + (self.last_name is None)
                + (self.date_of_birth is None)
                + (self.name is not None)
            )
            != 5
        ):
            raise ValueError("Invalid type of face and fields of this type")
        elif (
            self.type == TypeFace.natural
            and (
                (self.first_name is not None)
                + (self.second_name is not None)
                + (self.last_name is not None)
                + (self.date_of_birth is not None)
                + (self.name is None)
            )
            != 5
        ):
            raise ValueError("Invalid type of face and fields of this type")
        return self
