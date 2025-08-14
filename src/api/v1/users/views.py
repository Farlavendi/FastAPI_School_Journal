from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import ORJSONResponse

from src.api.v1.auth.dependencies import CurrentUserDep
from src.api.v1.auth.utils import logout
from src.core.db_utils import SessionDep
from src.core.models.users import RoleEnum
from . import crud
from .dependencies import UserByIdDep
from .schemas import User, UserUpdate

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
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
        response = ORJSONResponse(
            content={
                "next_step": "/api/users/students/create",
            }
        )
        # response = RedirectResponse(
        #     url="/docs#/Auth/create_user_student_api_v1_auth_register_student_post",
        #     status_code=status.HTTP_302_FOUND,
        # )
        return response

    elif role == RoleEnum.TEACHER:
        response = ORJSONResponse(
            content={
                "next_step": "/api/users/students/create",
            }
        )
        # response = RedirectResponse(
        #     url="/docs#/Auth/create_user_teacher_api_v1_auth_register_teacher_post",
        #     status_code=status.HTTP_302_FOUND,
        # )
        return response

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
    request: Request,
    response: Response,
):
    await logout(request=request, response=response)
    return await crud.delete_user(user=user, session=session)
