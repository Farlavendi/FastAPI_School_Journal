from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.core import config
from .schemas import TokenInfo
from .token_mixin import create_access_token, create_refresh_token
from .utils import (
    encode_jwt,
    CurrentUserDep,
    ValidateUserDep,
)

auth_jwt_config = config.AuthJWT()


class Token(BaseModel):
    access_token: str
    token_type: str


http_bearer = HTTPBearer(auto_error=False)
auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(http_bearer)],
)


@auth_router.post("/login/", response_model=TokenInfo)
async def issue_jwt(
    user: ValidateUserDep,
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user: ValidateUserDep
) -> Token:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_jwt_config.access_token_expire_minutes)
    access_token = encode_jwt(
        payload={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/users/me")
async def check_self_info(
    current_user: CurrentUserDep
):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "second_name": current_user.second_name,
        "last_name": current_user.last_name,
        "role": current_user.role
    }
