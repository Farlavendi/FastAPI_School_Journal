from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import Student, Marks
from .schemas import StudentCreate, StudentUpdate


async def create_student(
    session: AsyncSession,
    student_in: StudentCreate,
) -> Student:
    student = Student(**student_in.model_dump())
    session.add(student)
    await session.commit()
    return student


async def get_students(session: AsyncSession) -> Sequence[Student]:
    stmt = select(Student).order_by(Student.id)
    students = await session.scalars(stmt)
    return list(students)


async def get_student_by_id(session: AsyncSession, student_id: int) -> Student | None:
    return await session.get(Student, student_id)


async def get_marks(session: AsyncSession, student_id: int):
    stmt = (
        select(Marks)
        .join(Student, Student.id == Marks.student_id)
        .where(Student.id == student_id)
    )
    return await session.scalar(stmt)


async def update_student(
    session: AsyncSession,
    student: Student,
    student_update: StudentUpdate,
    partial: bool = False,
) -> Student:
    for username, value in student_update.model_dump(exclude_unset=partial).items():
        setattr(student, username, value)
    await session.commit()
    return student


async def delete_student(
    session: AsyncSession,
    student: Student,
) -> None:
    await session.delete(student)
    await session.commit()
