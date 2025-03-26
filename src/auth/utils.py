from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core import config, db_helper
from src.users import crud
from src.users.schemas import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login",
)
auth_jwt_config = config.AuthJWT()

class TokenData(BaseModel):
    username: str | None = None



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

    # to_encode.update(
    #     exp=expire_time,
    #     iat=now,
    #     jti=str(uuid.uuid4()),
    # )
    to_encode.update({"exp": expire_time})
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
        return jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )


# def hash_password(password: str) -> str:
#     return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#
#
# def validate_password(password: str, hashed_password: str) -> bool:
#     return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


async def get_token_payload(
    token: str = Depends(oauth2_scheme),
):
    try:
        return decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )


# async def validate_token_type(payload: dict, expected_type: str) -> bool:
#     current_token_type = payload.get("type")
#
#     if current_token_type != expected_type:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token type.",
#         )
#
#     return True


# async def get_user_by_token(
#     payload: dict = Depends(get_token_payload),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     await validate_token_type(payload=payload, expected_type="access")
#     user_id = payload.get("sub")
#
#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token: missing user ID.",
#         )
#
#     user = await crud.get_user_by_id(session=session, user_id=user_id)
#
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
#         )
#
#     return user

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            auth_jwt_config.public_key,
            algorithms=[auth_jwt_config.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await crud.get_user_by_username(session=session, username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await crud.get_user_by_username(session, username)

    # if not user or not validate_password(password, user.hashed_password):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive.",
        )

    return user
