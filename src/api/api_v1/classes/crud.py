from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.api_v1.models import Class
from .schemas import ClassCreate


async def get_classes(session: AsyncSession) -> Sequence[Class]:
    stmt = select(Class).order_by(Class.id)
    classes = await session.scalars(stmt)
    return list(classes)


async def get_class_by_id(session: AsyncSession, class_id: int) -> Class | None:
    return await session.get(Class, class_id)


async def get_class_by_num(
    session: AsyncSession,
    class_num: int,
) -> Class:
    stmt = (
        select(Class)
        .options(joinedload(Class.teacher))
        .where(Class.class_num == class_num)
    )

    class_: Class | None = await session.scalar(stmt)

    if class_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with number {class_num} not found",
        )

    return class_


async def create_class(session: AsyncSession, class_in: ClassCreate) -> Class:
    class_ = Class(**class_in.model_dump())
    session.add(class_)
    await session.commit()
    return class_


async def delete_class(
    session: AsyncSession,
    class_: Class,
) -> None:
    await session.delete(class_)
    await session.commit()
