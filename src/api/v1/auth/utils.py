from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from fastapi import HTTPException, Request, Response, status
from jwt import PyJWTError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.auth.schemas import TokenInfo
from src.api.v1.users.crud import get_user_by_username
from src.api.v1.users.schemas import User
from src.core.config import auth_jwt_config

password_hash = PasswordHash((
    Argon2Hasher(),
))


def encode_jwt(
    payload: dict,
    token_ttl: int,
    private_key: str = auth_jwt_config.private_key,
    algorithm: str = auth_jwt_config.algorithm,
    expires_delta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    jti = str(uuid4())

    if expires_delta:
        expire_time = now + expires_delta
    else:
        expire_time = now + timedelta(seconds=token_ttl)

    to_encode.update(
        {
            "exp": expire_time,
            "iat": now,
            "jti": jti
        },
    )
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded_jwt


def decode_jwt(
    token: str,
    public_key: str = auth_jwt_config.public_key,
    algorithm: str = auth_jwt_config.algorithm,
):
    try:
        payload = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def hash_password(password: str) -> str:
    return password_hash.hash(password=password)


def validate_password_hash(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(password=plain_password, hash=hashed_password)


async def get_token_payload(
    request: Request,
):
    token = request.cookies.get("access_token")

    try:
        return decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_token(
    token_type: str,
    token_data: dict,
    token_ttl: int,
    expires_delta: timedelta | None = None,
) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expires_delta=expires_delta,
        token_ttl=token_ttl
    )


def create_access_token(
    user: User,
) -> str:
    jwt_payload = {
        "sub": user.email,
        "user_id": str(user.id),
        "username": user.username,
    }
    return create_token(
        token_type="access",
        token_data=jwt_payload,
        token_ttl=auth_jwt_config.access_token_ttl,
    )


def create_refresh_token(
    user: User,
) -> str:
    jwt_payload = {
        "sub": user.username,
        "user_id": str(user.id),
    }
    return create_token(
        token_type="refresh",
        token_data=jwt_payload,
        token_ttl=auth_jwt_config.refresh_token_ttl,
    )


async def issue_tokens(
    user: User,
    response: Response,
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=auth_jwt_config.access_token_ttl,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=auth_jwt_config.refresh_token_ttl,
    )

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def refresh_access_token(session: AsyncSession, refresh_token: str) -> TokenInfo:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token",
        )
    try:
        payload = decode_jwt(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token type",
            )

        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token: missing username",
            )

        user = await get_user_by_username(session=session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        new_access_token = create_access_token(user)

        return TokenInfo(
            access_token=new_access_token,
            refresh_token=None,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error during token refresh: {str(e)}",
        )
