import sqlalchemy
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from . import crud
from .schemas import (
    Student,
    StudentCreate,
    StudentUpdate,
    StudentPartialUpdate,
)
from .dependencies import student_by_id

students_router = APIRouter(tags=["Students"])


@students_router.get("/", response_model=list[Student])
async def get_students(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_students(session=session)


@students_router.get("/{student_id}/", response_model=Student)
async def get_student_by_id(
    student: Student = Depends(student_by_id),
):
    return student


@students_router.get("/{student_id}/marks", response_model=Student)
async def get_marks(
    student_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_marks(student_id=student_id, session=session)


@students_router.post(
    "/create/",
    response_model=Student,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    student_in: StudentCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        return await crud.create_student(session=session, student_in=student_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student with this username or email already exists.",
        )


@students_router.put("/update/{student_id}/")
async def update_student(
    student_update: StudentUpdate,
    student: Student = Depends(student_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_student(
        session=session,
        student=student,
        student_update=student_update,
    )


@students_router.patch("/update/{student_id}/")
async def update_student_partial(
    student_update: StudentPartialUpdate,
    student: Student = Depends(student_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_student(
        session=session,
        student=student,
        student_update=student_update,
        partial=True,
    )


@students_router.delete("/delete/{student_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student: Student = Depends(student_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_student(
        session=session,
        student=student,
    )
