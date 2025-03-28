from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api.models import Class
from .schemas import ClassCreate


async def get_classes(session: AsyncSession) -> Sequence[Class]:
    stmt = select(Class)
    classes = await session.scalars(stmt)
    return list(classes)


async def get_class(
    session: AsyncSession,
    value: int,
    by_id: bool = False
) -> Class| None:

    query = select(Class).options(
            joinedload(Class.teacher),
            selectinload(Class.students)
    )

    if by_id:
        query = query.filter(Class.id == value)
    else:
        query = query.filter(Class.class_num == value)

    result = await session.execute(query)
    class_ = result.unique().scalar_one_or_none()

    if class_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found",
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
