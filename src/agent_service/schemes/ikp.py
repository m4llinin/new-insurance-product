from pydantic import BaseModel


class IkpScheme(BaseModel):
    id: int
    name: str
