from typing import List

from sqlalchemy import select
from src.api.models import Teacher
from .schemas import TeacherCreate, TeacherUpdate, TeacherPartialUpdate
from sqlalchemy.ext.asyncio import AsyncSession


async def create_teacher(
    session: AsyncSession,
    teacher_in: TeacherCreate,
) -> Teacher:
    teacher = Teacher(**teacher_in.model_dump())
    session.add(teacher)
    await session.commit()
    return teacher


async def get_teachers(session: AsyncSession) -> List[Teacher]:
    stmt = select(Teacher).order_by(Teacher.id)
    teachers = await session.scalars(stmt)
    return list(teachers)


async def get_teacher_by_id(session: AsyncSession, teacher_id: int) -> Teacher | None:
    return await session.get(Teacher, teacher_id)


async def update_teacher(
    session: AsyncSession,
    teacher: Teacher,
    teacher_update: TeacherUpdate | TeacherPartialUpdate,
    partial: bool = False,
) -> Teacher:
    for username, value in teacher_update.model_dump(exclude_unset=partial).items():
        setattr(teacher, username, value)
    await session.commit()
    return Teacher()


async def delete_teacher(
    session: AsyncSession,
    teacher: Teacher,
) -> None:
    await session.delete(teacher)
    await session.commit()
