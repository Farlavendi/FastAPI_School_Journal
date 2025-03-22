import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi.responses import RedirectResponse, ORJSONResponse
from src.core import db_helper
from . import crud
from .dependencies import user_by_id
from .schemas import User, UserCreate
from ..api.api_v1.models.users import RoleEnum
from ..api.api_v1.students.crud import create_student
from ..api.api_v1.students.schemas import StudentCreate
from ..api.api_v1.teachers.crud import create_teacher
from ..api.api_v1.teachers.schemas import TeacherCreate

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


@users_router.post("/choose-role")
async def choose_role(role: RoleEnum):
    if role == RoleEnum.STUDENT:
        return ORJSONResponse(
            content={
                "next_step": "/api/v1/users/create-student",
            }
        )
    elif role == RoleEnum.TEACHER:
        return ORJSONResponse(
            content={
                "next_step": "/api/v1/users/create-teacher",
            }
        )
    raise HTTPException(status_code=400, detail="Invalid role")


@users_router.post("/create-student")
async def create_user_student(
    user_in: UserCreate,
    student_in: StudentCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Создаёт юзера и затем студента."""
    try:
        user = await crud.create_user(session=session, user_in=user_in, role=RoleEnum.STUDENT)
        student = await create_student(session=session, student_in=student_in, user_id=user.id)
        await session.commit()
        return {"user": user, "student": student}
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Error creating student")


@users_router.post("/create-teacher")
async def create_user_teacher(
    user_in: UserCreate,
    teacher_in: TeacherCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Создаёт юзера и затем учителя."""
    try:
        user = await crud.create_user(session=session, user_in=user_in, role=RoleEnum.TEACHER)
        teacher = await create_teacher(session=session, teacher_in=teacher_in, user_id=user.id)
        await session.commit()
        return {"user": user, "teacher": teacher}
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Error creating teacher")


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
