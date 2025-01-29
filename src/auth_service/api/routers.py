from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from src.auth_service.services.auth import AuthService
from src.auth_service.api.dependencies import AuthUOWDep
from src.auth_service.schemes.auth import (
    AuthSchemeResponse,
    AuthSchemeIdResponse,
    AuthSchemeRequest,
)

from src.core.dependencies import TokenDep

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)


@router.post("/register", response_model=AuthSchemeIdResponse)
async def register(uow: AuthUOWDep, credentials: AuthSchemeRequest):
    try:
        user_id = await AuthService(uow).register_user(credentials)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return user_id


@router.post("/login", response_model=AuthSchemeResponse)
async def login(uow: AuthUOWDep, credentials: AuthSchemeRequest):
    try:
        tokens = await AuthService(uow).login_user(credentials)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return tokens


@router.post("/logout", response_model=AuthSchemeIdResponse)
async def logout(uow: AuthUOWDep, token: TokenDep):
    try:
        user_id = await AuthService(uow).logout_user(token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user_id


@router.post("/refresh", response_model=AuthSchemeResponse)
async def refresh(uow: AuthUOWDep, token: TokenDep):
    try:
        token = await AuthService(uow).refresh_token(token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return token
