from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.models import User, Student, Teacher
from src.api.models.users import RoleEnum
from .schemas import UserCreate, StudentUserCreate, TeacherUserCreate
from .student_schemas import StudentCreate
from .teacher_schemas import TeacherCreate


async def get_users(session: AsyncSession) -> Sequence[User]:
    stmt = (
        select(User)
        .options(joinedload(User.student), joinedload(User.teacher))  # eagerly load student and teacher
        .order_by(User.id)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users


async def get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(User)
        .filter(User.id == user_id)
        .options(
            joinedload(User.student),
            joinedload(User.teacher)
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

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

async def create_user_teacher(
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

async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
