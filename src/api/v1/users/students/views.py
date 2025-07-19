from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, HTTPException, Path, status

from src.api.v1.users.marks_schemas import Marks
from src.api.v1.users.schemas import StudentUserCreate
from src.core.db_utils import SessionDep
from src.tasks import send_welcome_email
from . import crud
from .schemas import StudentCreate, StudentUpdate, UserResponse

students_router = APIRouter(prefix="/students")


@students_router.get("/get/all", response_model=list[UserResponse])
async def get_students(
    session: SessionDep,
):
    return await crud.get_students(session=session)


@students_router.get("/marks/get", response_model=Marks)
async def get_marks(
    student_id: Annotated[int, Path],
    session: SessionDep,
):
    return await crud.get_marks(session=session, student_id=student_id)


@students_router.post("/create")
async def create_user_student(
    user_in: StudentUserCreate,
    student_in: StudentCreate,
    session: SessionDep,
):
    try:
        user = await crud.create_student(session=session, user_in=user_in, student_in=student_in)
        await session.commit()
        await send_welcome_email.kiq(user_id=user.id)
        return user
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating user.")


@students_router.patch("/update")
async def update_student(
    student: StudentUpdate,
    session: SessionDep,
):
    updated_student = await crud.update_student(
        session=session,
        student=student,
    )
    return updated_student
