from fastapi import Form, HTTPException, Request, Response

from src.api.v1.auth import auth_router
from src.api.v1.auth.jwt.schemas import TokenInfo
from src.api.v1.auth.jwt.utils import issue_tokens, refresh_access_token
from src.api.v1.auth.utils import validate_password_hash
from src.api.v1.users.crud import get_user_by_username
from src.core.config import auth_jwt_config
from src.core.db_utils import SessionDep


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


@auth_router.post("/logout")
async def delete_cookies(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}
