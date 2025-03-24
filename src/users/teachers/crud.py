from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.models import User, Teacher
from src.api.models.users import RoleEnum
from src.users.schemas import TeacherUserCreate
from src.users.teachers.schemas import TeacherCreate


async def get_teachers(session: AsyncSession) -> Sequence[User]:
    stmt = (
        select(User)
        .filter(User.role == RoleEnum.TEACHER)
        .options(joinedload(User.teacher))
        .order_by(User.id)
    )
    result = await session.execute(stmt)
    teachers = result.scalars().all()
    return teachers


async def create_teacher(
    session: AsyncSession,
    user_in: TeacherUserCreate,
    teacher_in: TeacherCreate
) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.flush()

    teacher = Teacher(user_id=user.id, **teacher_in.model_dump())
    session.add(teacher)

    return user