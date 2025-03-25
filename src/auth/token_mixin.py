from datetime import timedelta

from src.auth.utils import encode_jwt
from src.core import config
from src.users.schemas import User

auth_jwt_config = config.AuthJWT()


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = auth_jwt_config.access_token_expire_minutes,
    expires_delta: timedelta | None = None,
) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expires_delta=expires_delta,
    )


def create_access_token(
    user: User,
) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type="access",
        token_data=jwt_payload,
        expire_minutes=auth_jwt_config.access_token_expire_minutes,
    )


def create_refresh_token(
    user: User,
) -> str:
    jwt_payload = {
        "sub": user.username,
    }
    return create_jwt(
        token_type="refresh",
        token_data=jwt_payload,
        expire_minutes=auth_jwt_config.access_token_expire_minutes * 60 * 24,
    )
