from fastapi import APIRouter, Form, Request, Response

from src.api.v1.auth import utils
from src.api.v1.auth.dependencies import validate_user
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
    await validate_user(session, username, password)

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
