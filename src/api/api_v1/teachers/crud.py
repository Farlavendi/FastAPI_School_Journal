from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.api_v1.models import Teacher
from .schemas import TeacherCreate, TeacherUpdate
from ..models.users import RoleEnum


async def create_teacher(
    user_id: int,
    session: AsyncSession,
    teacher_in: TeacherCreate,
) -> Teacher:
    teacher = Teacher(user_id=user_id, **teacher_in.model_dump())
    session.add(teacher)
    await session.commit()
    return teacher


async def get_teachers(session: AsyncSession) -> Sequence[Teacher]:
    stmt = select(Teacher).order_by(Teacher.id)
    teachers = await session.scalars(stmt)
    return list(teachers)


async def get_teacher_by_id(session: AsyncSession, teacher_id: int) -> Teacher | None:
    return await session.get(Teacher, teacher_id)


async def update_teacher(
    session: AsyncSession,
    teacher: Teacher,
    teacher_update: TeacherUpdate,
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
