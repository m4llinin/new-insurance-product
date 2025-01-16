from fastapi import APIRouter, HTTPException, status

from src.auth_service.services.auth import AuthService
from src.auth_service.api.dependencies import AuthUOWDep
from src.auth_service.schemas.auth import (
    AuthSchemeResponse,
    AuthSchemeIdResponse,
    AuthSchemeRequest,
)

from src.core.dependencies import TokenDep

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)


@router.post("/register")
async def register(
    uow: AuthUOWDep, credentials: AuthSchemeRequest
) -> AuthSchemeIdResponse:
    try:
        user_id = await AuthService(uow).register_user(credentials)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return user_id


@router.post("/login")
async def login(uow: AuthUOWDep, credentials: AuthSchemeRequest) -> AuthSchemeResponse:
    try:
        tokens = await AuthService(uow).login_user(credentials)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return tokens


@router.post("/logout")
async def logout(uow: AuthUOWDep, token: TokenDep) -> AuthSchemeIdResponse:
    try:
        user_id = await AuthService(uow).logout_user(token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user_id


@router.post("/refresh")
async def refresh(uow: AuthUOWDep, token: TokenDep) -> AuthSchemeResponse:
    try:
        token = await AuthService(uow).refresh_token(token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return token
