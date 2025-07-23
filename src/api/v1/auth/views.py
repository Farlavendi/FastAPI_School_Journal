from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.security import HTTPBearer

from src.api.v1.users.crud import get_user_by_username
from src.core.config import auth_jwt_config
from src.core.db_utils import SessionDep
from .dependencies import CurrentUserDep
from .schemas import TokenInfo
from .utils import issue_tokens, refresh_access_token, validate_password_hash

http_bearer = HTTPBearer(auto_error=False)
auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(http_bearer)],
)


@auth_router.get("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
async def refresh_jwt(
    request: Request,
    response: Response,
    session: SessionDep,
):
    refresh_token = request.cookies.get("refresh_token")

    token_info = await refresh_access_token(session=session, refresh_token=refresh_token)

    response.set_cookie(
        key="access_token",
        value=token_info.access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=auth_jwt_config.access_token_ttl,
    )

    return token_info


@auth_router.post("/login", response_model=None)
async def login(
    response: Response,
    session: SessionDep,
    password: str = Form(...),
    username: str = Form(...),
):
    user = await get_user_by_username(session=session, username=username)
    if not validate_password_hash(plain_password=password, hashed_password=user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    else:
        return await issue_tokens(user=user, response=response)


@auth_router.get("/users/me")
async def check_self_info(
    current_user: CurrentUserDep,
):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "second_name": current_user.second_name,
        "last_name": current_user.last_name,
        "role": current_user.role,
    }


@auth_router.post("/logout")
async def delete_cookies(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}
