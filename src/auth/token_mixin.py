from datetime import timedelta

from auth.utils import encode_jwt
from users.schemas import UserSchemaForAuth
from core.config import AuthJWT


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: AuthJWT().access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(
    user: UserSchemaForAuth,
) -> str:
    jwt_payload = {
        # "sub": user.id,
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type="access",
        token_data=jwt_payload,
        expire_minutes=AuthJWT().access_token_expire_minutes,
    )


def create_refresh_token(
    user: UserSchemaForAuth,
) -> str:
    jwt_payload = {
        "sub": user.username,
    }
    return create_jwt(
        token_type="refresh",
        token_data=jwt_payload,
        expire_minutes=timedelta(days=AuthJWT().refresh_token_expire_days),
    )
