from typing import Annotated
from datetime import datetime

from fastapi import (
    Header,
    Request,
    Depends,
)
from faststream.rabbit.fastapi import RabbitBroker
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func


def _get_broker(request: Request) -> RabbitBroker:
    return request.state.broker


TokenDep = Annotated[str, Header(alias="WWW-Authorization")]
BrokerDep = Annotated[RabbitBroker, Depends(_get_broker)]

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
int_not_null = Annotated[int, mapped_column(nullable=False)]
str_not_null = Annotated[str, mapped_column(nullable=False)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(server_default=func.now(), server_onupdate=func.now())
]
