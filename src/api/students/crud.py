from typing import List

from sqlalchemy import select, Result

from .schemas import Student, StudentCreate, StudentUpdate, StudentPartialUpdate
from sqlalchemy.ext.asyncio import AsyncSession


async def create_student(session: AsyncSession, student_in: StudentCreate) -> Student:
    student = Student(**student_in.model_dump())
    session.add(student)
    await session.commit()
    return student


async def get_students(session: AsyncSession) -> List[Student]:
    stmt = select(Student).order_by(Student.id)
    result: Result = await session.execute(stmt)
    students = result.scalars().all()
    return list(students)


async def get_student_by_id(session: AsyncSession, student_id: int) -> Student | None:
    return await session.get(Student, student_id)


async def update_student(
    session: AsyncSession,
    student: Student,
    student_update: StudentUpdate | StudentPartialUpdate,
    partial: bool = False,
) -> Student:
    for name, value in student_update.model_dump(exclude_unset=partial).items():
        setattr(student, name, value)
    await session.commit()
    return student


async def delete_student(
    session: AsyncSession,
    student: Student,
) -> None:
    await session.delete(student)
    await session.commit()
