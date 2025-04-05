from typing import Annotated, Optional

import sqlalchemy
from fastapi import APIRouter, HTTPException, status, Path

from src.api.models.teachers import SubjectEnum
from src.core.db_utils import SessionDep
from src.users.schemas import TeacherUserCreate
from src.users.teachers import crud
from src.users.teachers.crud import create_teacher
from src.users.teachers.schemas import TeacherCreate, UserResponse

teachers_router = APIRouter(prefix="/teachers")


@teachers_router.get("/get-teachers", response_model=list[UserResponse])
async def get_teachers(
    session: SessionDep,
):
    return await crud.get_teachers(session=session)


@teachers_router.post("/create-teacher")
async def create_user_teacher(
    user_in: TeacherUserCreate,
    teacher_in: TeacherCreate,
    session: SessionDep,
    subject: Optional[Annotated[SubjectEnum, Path]] = None,
):
    try:
        user = await create_teacher(session=session, user_in=user_in, teacher_in=teacher_in, subject=subject)
        await session.commit()
        return user
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating user.")
