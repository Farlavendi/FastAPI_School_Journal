import hashlib
import hmac
from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException, Response, status
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.auth.dependencies import validate_user
from src.api.v1.users.crud import get_user_by_username
from src.core.config import redis_client, settings

password_hash = PasswordHash((
    Argon2Hasher(),
))

SECRET_KEY = settings.auth.secret_key
SESSION_TTL = settings.auth.session_ttl


def hash_password(password: str) -> str:
    return password_hash.hash(password=password)


def validate_password_hash(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(password=plain_password, hash=hashed_password)


def sign_session_id(session_id: str) -> str:
    signature = hmac.new(
        key=SECRET_KEY,
        msg=session_id.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    return f"{session_id}.{signature}"


def verify_session_token(token: str) -> str | None:
    try:
        session_id, sig = token.rsplit('.', 1)
        expected_sig = hmac.new(
            key=SECRET_KEY,
            msg=session_id.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(sig, expected_sig):
            return session_id

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session token format.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Session verification error: {e}",
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid session token signature.",
    )


async def login(
    session: AsyncSession,
    response: Response,
    username: str,
    password: str,
):
    await validate_user(session, username, password)

    user = await get_user_by_username(session, username)
    session_id = sign_session_id(str(uuid4()))

    redis_key = f"session:{session_id}"

    await redis_client.hset(
        redis_key,
        mapping={
            "user_id": str(user.id),
            "created_at": datetime.now().isoformat(),
        }
    )
    await redis_client.expire(redis_key, SESSION_TTL)
    await redis_client.set("session_id", session_id)
    await redis_client.sadd(f"user_sessions:{user.id}", session_id)

    response.set_cookie(
        key="session_token",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=SESSION_TTL
    )
