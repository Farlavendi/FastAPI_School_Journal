from fastapi import APIRouter, Form, HTTPException, Request, Response, status
from sqlalchemy import update

from src.api.v1.auth import utils
from src.api.v1.auth.dependencies import validate_user
from src.api.v1.auth.utils import verify_session_token
from src.core.config import redis_client
from src.core.db_utils import SessionDep
from src.core.models import User
from src.tasks import send_verification_email

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post('/login')
async def login(
    session: SessionDep,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),

):
    user = await validate_user(session, username, password)
    await send_verification_email.kiq(user_id=user.id)

    return await utils.login(
        session=session,
        response=response,
        username=username,
    )


@auth_router.post("/logout")
async def logout(response: Response, request: Request):
    return await utils.logout(request=request, response=response)


@auth_router.post("/logout_all")
async def logout_all(request: Request, response: Response):
    return await utils.logout_all(request=request, response=response)


@auth_router.get("/verify-email")
async def verify_email(
    verification_token: str,
    request: Request,
    session: SessionDep,
):
    token = request.cookies.get("session_token")
    user_id_redis = await redis_client.get(f"verification_token:{verification_token}")
    user_id_cookies, _ = await verify_session_token(token)

    if not user_id_redis:
        raise HTTPException(400, "Invalid or expired token")

    if user_id_redis.decode("utf-8") == user_id_cookies:
        await redis_client.delete(f"verification_token:{verification_token}")

        await session.execute(
            update(User)
            .where(User.id == user_id_cookies)
            .values(is_verified=True)
        )
        await session.commit()

        return {"message": f"Email verified successfully for user with id: {user_id_cookies}"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email verification failed.",
    )
