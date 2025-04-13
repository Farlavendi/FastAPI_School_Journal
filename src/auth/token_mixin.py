from datetime import timedelta

from fastapi import HTTPException, status

from src.auth.schemas import TokenInfo
from src.auth.utils import encode_jwt, decode_jwt
from src.core import config
from src.core.db_utils import SessionDep
from src.users.crud import get_user_by_username
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


async def refresh_jwt_token(session: SessionDep, refresh_token: str) -> TokenInfo:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token"
        )
    try:
        payload = decode_jwt(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token type"
            )

        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token: missing username"
            )

        user = await get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        new_access_token = create_access_token(user)

        return TokenInfo(
            access_token=new_access_token,
            refresh_token=None,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error during token refresh: {str(e)}"
        )
