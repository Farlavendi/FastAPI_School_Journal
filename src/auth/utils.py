from datetime import timedelta, datetime, timezone

import bcrypt
import jwt

from src.core import config


def encode_jwt(
    payload: dict,
    private_key: str = config.AuthJWT.private_key,
    algorithm: str = config.AuthJWT.algorithm,
    expire_minutes: int = config.AuthJWT.expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)

    if expire_timedelta:
        expire_time = now + expire_timedelta
    else:
        expire_time = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire_time,
        iat=now,
    )

    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = config.AuthJWT.public_key,
    algorithm: str = config.AuthJWT.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
