from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import User, Student
from src.api.models.users import RoleEnum
from .schemas import UserCreate, StudentUserCreate
from ..api.students.schemas import StudentCreate


async def get_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    classes = await session.scalars(stmt)
    return list(classes)


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
    role: RoleEnum
) -> User:
    user = User(role=role, **user_in.model_dump())
    session.add(user)
    await session.commit()
    return user

async def create_user_student(
    session: AsyncSession,
    user_in: StudentUserCreate,
    student_in: StudentCreate
) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.flush()

    student = Student(user_id=user.id, **student_in.model_dump())
    session.add(student)

    return user

async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
