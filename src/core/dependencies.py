from typing import Annotated
from datetime import datetime
from fastapi import (
    Header,
    Depends,
)
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from src.core.config import Config
from src.core.rabbit.broker import BrokerRabbit


def _get_broker() -> BrokerRabbit:
    return BrokerRabbit(Config().rmq.URL)


TokenDep = Annotated[str, Header(alias="WWW-Authorization")]
BrokerDep = Annotated[BrokerRabbit, Depends(_get_broker)]

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
int_not_null = Annotated[int, mapped_column(nullable=False)]
str_not_null = Annotated[str, mapped_column(nullable=False)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(server_default=func.now(), server_onupdate=func.now())
]
