from typing import List

from sqlalchemy import select
from src.api.models import Student
from .schemas import StudentCreate, StudentUpdate, StudentPartialUpdate
from sqlalchemy.ext.asyncio import AsyncSession


async def create_student(session: AsyncSession, student_in: StudentCreate) -> Student:
    student = Student(**student_in.model_dump())
    session.add(student)
    await session.commit()
    return student


async def get_students(session: AsyncSession) -> List[Student]:
    stmt = select(Student).order_by(Student.id)
    students = await session.scalars(stmt)
    return list(students)


async def get_student_by_id(session: AsyncSession, student_id: int) -> Student | None:
    return await session.get(Student, student_id)


async def update_student(
    session: AsyncSession,
    student: Student,
    student_update: StudentUpdate | StudentPartialUpdate,
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
