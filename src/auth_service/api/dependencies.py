from fastapi import Depends
from typing import Annotated

from src.auth_service.utils.uow import AuthUOW

AuthUOWDep = Annotated[AuthUOW, Depends(AuthUOW)]

