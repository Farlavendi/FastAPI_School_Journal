from typing import Annotated

import jwt
from fastapi import Depends, Form, HTTPException, Request
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from starlette import status

from src.api.v1.auth.utils import validate_password_hash
from src.api.v1.users import crud
from src.api.v1.users.schemas import User
from src.core.config import auth_jwt_config
from src.core.db_utils import SessionDep


async def get_current_user(
    response: Request,
    session: SessionDep,
):
    token = response.cookies.get("access_token")

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
