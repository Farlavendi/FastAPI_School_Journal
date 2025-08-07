from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError

from src.api.v1.auth.dependencies import CurrentUserDep
from src.api.v1.auth.views import auth_router
from src.api.v1.models.teachers import SubjectEnum
from src.api.v1.users.marks_schemas import MarksUpdate
from src.api.v1.users.schemas import TeacherUserCreate
from src.core.db_utils import SessionDep
from src.tasks import send_welcome_email
from . import crud
from .schemas import TeacherCreate, TeacherUpdate, UserResponse

teachers_router = APIRouter(prefix="/teachers", tags=["Teachers"])


@teachers_router.get("/get/all", response_model=list[UserResponse])
async def get_teachers(
    session: SessionDep,
):
    return await crud.get_teachers(session=session)


@auth_router.post("/register/teacher")
async def create_user_teacher(
    user_in: TeacherUserCreate,
    teacher_in: TeacherCreate,
    session: SessionDep,
    subject: Annotated[SubjectEnum, Path] | None = None,
):
    try:
        user = await crud.create_teacher(
            session=session,
            user_in=user_in,
            teacher_in=teacher_in,
            subject=subject,
        )
        await session.commit()
        await send_welcome_email.kiq(user_id=user.id)
        return user
    except IntegrityError:
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
        marks=marks,
    )

    return updated_marks
