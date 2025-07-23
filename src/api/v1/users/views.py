from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from starlette import status

from src.api.v1.auth.dependencies import CurrentUserDep
from src.api.v1.auth.views import http_bearer
from src.core.db_utils import SessionDep
from src.core.models.users import RoleEnum
from . import crud
from .dependencies import UserByIdDep
from .schemas import User, UserUpdate

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(http_bearer)],
)


@users_router.get("/get/all", response_model=list[User], response_model_exclude_none=True)
async def get_users(
    session: SessionDep,
):
    return await crud.get_users(session=session)


@users_router.get("/get/{users_id}", response_model=User, response_model_exclude_none=True)
async def get_user_by_id(
    user: UserByIdDep,
):
    return user


@users_router.post("/choose-role")
async def choose_role(role: RoleEnum):
    if role == RoleEnum.STUDENT:
        return ORJSONResponse(
            content={
                "next_step": "/api/users/students/create",
            },
        )
    elif role == RoleEnum.TEACHER:
        return ORJSONResponse(
            content={
                "next_step": "/api/users/teachers/create",
            },
        )
    elif role == RoleEnum.SUPERUSER:
        return ORJSONResponse(
            content={
                "next_step": "/api/users/create-superuser",  # TODO create a superuser creation logic
            }
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid role")


@users_router.get("/me")
async def auth_user_check_self_info(
    current_user: CurrentUserDep,
):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "second_name": current_user.second_name,
        "last_name": current_user.last_name,
        "role": current_user.role,
    }


@users_router.patch("/profile/edit", response_model=UserUpdate)
async def update_user(
    user_update: UserUpdate,
    session: SessionDep,
    user: CurrentUserDep,
):
    updated_user = await crud.update_user(
        session=session,
        user_id=user.id,
        user_in=user_update,
    )
    return updated_user


@users_router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    session: SessionDep,
    user: UserByIdDep,
):
    return await crud.delete_user(user=user, session=session)
