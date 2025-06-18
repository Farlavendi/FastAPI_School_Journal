from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, HTTPException, status, Path, BackgroundTasks

from src.api.v1.users.marks_schemas import Marks
from src.api.v1.users.schemas import StudentUserCreate
from src.core.db_utils import SessionDep
from src.mailing.send_welcome_email import send_welcome_email
from . import crud
from .schemas import StudentCreate, UserResponse

students_router = APIRouter(prefix="/students")


@students_router.get("/get-students", response_model=list[UserResponse])
async def get_students(
    session: SessionDep,
):
    return await crud.get_students(session=session)


@students_router.get("/get-marks", response_model=Marks)
async def get_marks(
    student_id: Annotated[int, Path],
    session: SessionDep,
):
    return await crud.get_marks(session=session, student_id=student_id)


@students_router.post("/create-student")
async def create_user_student(
    user_in: StudentUserCreate,
    student_in: StudentCreate,
    session: SessionDep,
    background_tasks: BackgroundTasks,
):
    try:
        user = await crud.create_student(session=session, user_in=user_in, student_in=student_in)
        await session.commit()
        background_tasks.add_task(send_welcome_email, user.id)
        return user
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating user.")
