from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import HTTPBearer

from src.core import config
from .schemas import TokenInfo
from .token_mixin import create_access_token, create_refresh_token, refresh_jwt_token
from .utils import CurrentUserDep, ValidateUserDep

auth_jwt_config = config.AuthJWT()

http_bearer = HTTPBearer(auto_error=False)
auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(http_bearer)],
)


@auth_router.get("/refresh", response_model=TokenInfo)
async def refresh_jwt(
    request: Request,
    response: Response,
):
    refresh_token = request.cookies.get("refresh_token")

    token_info = await refresh_jwt_token(refresh_token)

    response.set_cookie(
        key="access_token",
        value=token_info.access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=auth_jwt_config.access_token_expire_minutes * 60
    )

    return token_info


@auth_router.post("/login/", response_model=TokenInfo)
async def issue_jwt(
    user: ValidateUserDep,
    response: Response
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=auth_jwt_config.access_token_expire_minutes * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=auth_jwt_config.access_token_expire_minutes * 60 * 24
    )

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


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


@auth_router.post("/logout")
async def delete_cookies(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}
