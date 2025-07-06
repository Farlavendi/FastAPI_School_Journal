from typing import Annotated, Optional

import sqlalchemy
from fastapi import APIRouter, HTTPException, status, Path

from src.api.v1.models.teachers import SubjectEnum
from src.api.v1.users.marks_schemas import MarksUpdate
from src.api.v1.users.schemas import TeacherUserCreate
from src.auth.utils import CurrentUserDep
from src.core.db_utils import SessionDep
from src.tasks import send_welcome_email
from . import crud
from .schemas import TeacherCreate, UserResponse, TeacherUpdate

teachers_router = APIRouter(prefix="/teachers")


@teachers_router.get("/get/all", response_model=list[UserResponse])
async def get_teachers(
    session: SessionDep,
):
    return await crud.get_teachers(session=session)


@teachers_router.post("/create")
async def create_user_teacher(
    user_in: TeacherUserCreate,
    teacher_in: TeacherCreate,
    session: SessionDep,
    subject: Optional[Annotated[SubjectEnum, Path]] = None,
):
    try:
        user = await crud.create_teacher(session=session, user_in=user_in, teacher_in=teacher_in, subject=subject)
        await session.commit()
        await send_welcome_email.kiq(user_id=user.id)
        return user
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating user.")


@teachers_router.patch("/update")
async def update_teacher(
    session: SessionDep,
    teacher: TeacherUpdate,
    subject: SubjectEnum,
):
    updated_subject = await crud.update_teacher(
        session=session,
        teacher=teacher,
        subject=subject,
    )
    return updated_subject


@teachers_router.patch("/marks/edit")
async def update_marks(
    session: SessionDep,
    user: CurrentUserDep,
    marks: MarksUpdate,
):
    updated_marks = await crud.update_marks(
        session=session,
        user=user,
        marks=marks
    )

    return updated_marks
