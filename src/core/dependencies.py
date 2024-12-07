from typing import Annotated
from datetime import datetime

from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_not_null = Annotated[str, mapped_column(nullable=False)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), server_onupdate=func.now())]
