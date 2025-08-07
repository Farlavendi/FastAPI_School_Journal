from fastapi import APIRouter, Form, HTTPException, Request, Response, status

from src.api.v1.auth import utils
from src.api.v1.auth.utils import verify_session_token
from src.core.config import redis_client
from src.core.db_utils import SessionDep

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
    await utils.login(
        session=session,
        response=response,
        username=username,
        password=password,
    )

    return {"message": "Logged in successfully"}


@auth_router.post("/logout")
async def logout(response: Response, request: Request):
    token = request.cookies.get("session_token")
    session_id = verify_session_token(token) if token else None
    if session_id:
        redis_key = f"session:{session_id}"
        user_id = await redis_client.hget(redis_key, "user_id")
        await redis_client.delete(redis_key)
        if user_id:
            await redis_client.srem(f"user_sessions:{user_id}", session_id)
        response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}


@auth_router.post("/logout_all")
async def logout_all(request: Request):
    token = request.cookies.get("session_token")
    session_id = verify_session_token(token) if token else None
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    redis_key = f"session:{session_id}"
    user_id = await redis_client.hget(redis_key, "user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    session_ids = await redis_client.smembers(f"user_sessions:{user_id}")
    for sid in session_ids:
        await redis_client.delete(f"session:{sid}")
    await redis_client.delete(f"user_sessions:{user_id}")

    return {"message": "Logged out from all devices"}
