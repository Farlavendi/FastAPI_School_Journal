from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from . import crud
from .schemas import Student, StudentCreate, StudentUpdate, StudentPartialUpdate


students_router = APIRouter(tags=["Students"])


@students_router.get("/", response_model=list[Student])
async def get_students(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_students(session=session)


@students_router.post(
    "/create/", response_model=Student, status_code=status.HTTP_201_CREATED
)
async def create_student(
    student_in: StudentCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_student(session=session, student_in=student_in)


@students_router.get("/{student_id}/", response_model=Student)
async def get_student_by_id(
    student_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    student = await crud.get_student_by_id(session=session, student_id=student_id)
    if student is not None:
        return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student with id {student_id} not found.",
    )
