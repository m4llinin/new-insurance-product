from pydantic import BaseModel


class LobScheme(BaseModel):
    id: int
    name: str
