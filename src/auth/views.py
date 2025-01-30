from fastapi import APIRouter, Depends

from auth.utils import validate_auth_user, get_current_active_user
from src.auth import utils as auth_utils
from src.auth.schemas import TokenInfo
from src.users.schemas import UserSchemaForAuth

auth_router = APIRouter(prefix="/jwt", tags=["JWT"])


@auth_router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchemaForAuth = Depends(validate_auth_user),
):
    jwt_payload = {
        # "sub": user.id,
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }

    token = auth_utils.encode_jwt(jwt_payload)

    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@auth_router.post("/users/me")
def auth_user_check_self_info(
    user: UserSchemaForAuth = Depends(get_current_active_user),
):
    return {
        "username": user.username,
        "email": user.email,
    }
