import hashlib
import hmac
from uuid import uuid4

from fastapi import HTTPException, Request, Response, status
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from sqlalchemy.ext.asyncio import AsyncSession

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


def sign_token(token: str) -> str:
    signature = hmac.new(
        key=SECRET_KEY,
        msg=token.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    return f"{token}.{signature}"


async def verify_session_token(token: str) -> tuple[str, str]:
    try:
        token, sig = token.rsplit('.', 1)
        user_id, session_id = token.split('|', 1)

        expected_sig = hmac.new(
            key=SECRET_KEY,
            msg=token.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        redis_entry_exists = await redis_client.exists(f"session:{session_id}")

        if not redis_entry_exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired or invalid"
            )

        if hmac.compare_digest(sig, expected_sig) and redis_entry_exists:
            return user_id, session_id

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
    username: str
):
    user = await get_user_by_username(session, username)

    session_id = uuid4().hex
    token = f"{str(user.id)}|{session_id}"

    await redis_client.set(f"session:{session_id}", str(user.id), ex=SESSION_TTL)
    await redis_client.sadd(f"user_sessions:{str(user.id)}", session_id)

    signed_token = sign_token(token)

    response.set_cookie(
        key="session_token",
        value=signed_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=SESSION_TTL
    )

    return {"message": "Logged in successfully"}


async def logout(
    request: Request,
    response: Response,
):
    token = request.cookies.get("session_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Already logged out."
        )

    user_id, session_id = await verify_session_token(token)

    await redis_client.delete(f"session:{session_id}")
    await redis_client.srem(f"user_sessions:{user_id}", session_id)

    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}


async def logout_all(
    request: Request,
    response: Response,
):
    token = request.cookies.get("session_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Already logged out."
        )

    user_id, session_id = await verify_session_token(token)

    # session_ids = await redis_client.smembers(f"user_sessions:{user_id}")
    #
    # for sid in session_ids:
    #     await redis_client.delete(f"session:{sid.decode('utf-8')}")
    #
    # await redis_client.delete(f"user_sessions:{user_id}")

    lua_script = """
        local user_sessions_key = KEYS[1]
        local session_ids = redis.call("SMEMBERS", user_sessions_key)

        for _, sid in ipairs(session_ids) do
            redis.call("DEL", "session:" .. sid)
        end

        redis.call("DEL", user_sessions_key)
        """
    await redis_client.eval(lua_script, 1, f"user_sessions:{user_id}")

    response.delete_cookie("session_token")
    return {"message": "Logged out from all devices"}
