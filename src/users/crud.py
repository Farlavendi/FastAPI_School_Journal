from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.api_v1.models import User
from .schemas import UserCreate, StudentUserCreate
from ..api.api_v1.models.users import RoleEnum


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
) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    return user

async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
