from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from .utils import validate_auth_user, get_current_active_user, UserGetterFromToken
from .schemas import TokenInfo
from users.schemas import UserSchemaForAuth
from .token_mixin import create_access_token, create_refresh_token

http_bearer = HTTPBearer(auto_error=False)
auth_router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


@auth_router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchemaForAuth = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@auth_router.post(
    "/refresh/", response_model=TokenInfo, response_model_exclude_none=True
)
def refresh_jwt(user: UserSchemaForAuth = Depends(UserGetterFromToken("refresh"))):
    access_token = create_access_token(user)

    return TokenInfo(
        access_token=access_token,
    )


@auth_router.post("/users/me")
def auth_user_check_self_info(
    user: UserSchemaForAuth = Depends(get_current_active_user),
):
    return {
        "username": user.username,
        "email": user.email,
    }
