from typing import Sequence

from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.api_v1.models import User
from .schemas import UserCreate


async def get_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    classes = await session.scalars(stmt)
    return list(classes)


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(session: AsyncSession, user_in: UserCreate) -> User | RedirectResponse:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
