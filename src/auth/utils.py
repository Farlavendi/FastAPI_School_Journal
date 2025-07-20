from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pydantic import ValidationError
from starlette import status

from src.api.v1.users import crud
from src.api.v1.users.schemas import User
from src.core import config
from src.core.db_utils import SessionDep

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)

password_hash = PasswordHash((
    Argon2Hasher(),
))

auth_jwt_config = config.AuthJWT()


def encode_jwt(
    payload: dict,
    private_key: str = auth_jwt_config.private_key,
    algorithm: str = auth_jwt_config.algorithm,
    expire_minutes: int = auth_jwt_config.access_token_expire_minutes,
    expires_delta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire_time = now + expires_delta
    else:
        expire_time = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        {
            "exp": expire_time,
            "iat": now,
            "jti": str(uuid4())
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
    token: str = Depends(oauth2_scheme),
):
    try:
        return decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(
            token,
            auth_jwt_config.public_key,
            algorithms=[auth_jwt_config.algorithm],
        )
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = await crud.get_user_by_username(session=session, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def validate_user(
    session: SessionDep,
    username: str = Form(),
    password: str = Form(),
):
    user = await crud.get_user_by_username(session, username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not validate_password_hash(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
ValidateUserDep = Annotated[User, Depends(validate_user)]
