from typing import Sequence
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.models import User
from .schemas import UserUpdate


async def get_users(session: AsyncSession) -> Sequence[User]:
    stmt = (
        select(User)
        .options(
            joinedload(User.student),
            joinedload(User.teacher),
        )
        .order_by(User.id)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users


async def get_user_by_id(session: AsyncSession, user_id: UUID):
    result = await session.execute(
        select(User)
        .where(User.id == user_id)
        .options(
            joinedload(User.student),
            joinedload(User.teacher),
        ),
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(
        select(User)
        .where(User.username == username),
    )
    return result.scalar_one_or_none()


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()


async def update_user(
    session: AsyncSession,
    user_id: UUID,
    user_in: UserUpdate,
):
    result = await session.execute(
        update(User)
        .where(User.id == user_id)
        .values(**user_in.model_dump(exclude_unset=True))
        .returning(User),
    )
    await session.commit()
    return result.scalar_one()
