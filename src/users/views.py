import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import db_helper
from . import crud
from .dependencies import user_by_id
from .schemas import User, UserCreate

users_router = APIRouter(tags=["Users"])


@users_router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@users_router.get("/{users_id}", response_model=User)
async def get_user_by_id(
    user: User = Depends(user_by_id),
):
    return user


@users_router.post("/create", response_model=User)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        return await crud.create_user(session=session, user_in=user_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this number already exists.",
        )


@users_router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_user(user=user, session=session)
