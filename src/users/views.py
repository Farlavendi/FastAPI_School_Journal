from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.models.users import RoleEnum
from src.core import db_helper
from . import crud
from .dependencies import user_by_id
from .schemas import User

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/", response_model=list[User], response_model_exclude_none=True)
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@users_router.get("/{users_id}", response_model=User, response_model_exclude_none=True)
async def get_user_by_id(
    user: User = Depends(user_by_id),
):
    return user


@users_router.post("/choose-role")
async def choose_role(role: RoleEnum):
    if role == RoleEnum.STUDENT:
        return ORJSONResponse(
            content={
                "next_step": "/api/users/create-student",
            }
        )
    elif role == RoleEnum.TEACHER:
        return ORJSONResponse(
            content={
                "next_step": "/api/users/create-teacher",
            }
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid role")


@users_router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_user(user=user, session=session)
