from fastapi import APIRouter, Depends, Form, HTTPException
from starlette import status

from src.users.schemas import User
from src.auth import utils as auth_utils
from src.auth.schemas import TokenInfo

router = APIRouter(prefix="/jwt", tags=["JWT"])

users_db: dict[str, User] = {

}


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

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password
    ):
        return unauthorized_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    raise user


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: User = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
    }

    token = auth_utils.encode_jwt(jwt_payload)

    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
