from datetime import timedelta, datetime, timezone
from jwt.exceptions import InvalidTokenError
import bcrypt
import jwt
from fastapi import HTTPException, Depends, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from starlette import status

from src.core import config
from users.schemas import UserSchemaForAuth

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login",
)


def encode_jwt(
    payload: dict,
    private_key: str = config.AuthJWT().private_key_path.read_text(),
    algorithm: str = config.AuthJWT().algorithm,
    expire_minutes: int = config.AuthJWT().access_token_expire_minutes,
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
    public_key: str = config.AuthJWT().public_key_path.read_text(),
    algorithm: str = config.AuthJWT().algorithm,
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


sam = UserSchemaForAuth(
    email="email@gmail.com",
    username="samio",
    hashed_password=hash_password("sam123"),
    first_name="sam",
    second_name="",
    last_name="johnson",
)

users_db: dict[str, UserSchemaForAuth] = {
    sam.username: sam,
}


def get_token_payload(
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )
    return payload


def get_current_user(
    payload: dict = Depends(get_token_payload),
) -> UserSchemaForAuth:
    username: str | None = payload.get("username")

    if user := users_db.get(username):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        # actually 404 not found but user doesn't need to know this imho.
        detail="Invalid token.",
    )


def get_current_active_user(
    user: UserSchemaForAuth = Depends(get_current_user),
):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive.",
        )
    return user


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )

    if not (user := users_db.get(username)):
        raise unauthorized_exception

    if not validate_password(password=password, hashed_password=user.hashed_password):
        return unauthorized_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive.",
        )
    return user
