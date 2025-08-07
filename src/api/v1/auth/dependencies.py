from typing import Annotated

from fastapi import Depends, Form, HTTPException, Request, status

from src.api.v1.auth.utils import validate_password_hash, verify_session_token
from src.api.v1.users import crud
from src.api.v1.users.crud import get_user_by_id
from src.core.config import redis_client
from src.core.db_utils import SessionDep
from src.core.models import User


async def get_current_user(
    request: Request,
    session: SessionDep
) -> dict:
    token = request.cookies.get("session_token")
    session_id = verify_session_token(token) if token else None
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

    redis_key = f"session:{session_id}"
    session_data = await redis_client.hgetall(redis_key)
    if not session_data or "user_id" not in session_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid")

    user_id = session_data["user_id"]
    user = await get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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
        )

    if not validate_password_hash(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive.",
        )
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
ValidateUserDep = Annotated[User, Depends(validate_user)]
