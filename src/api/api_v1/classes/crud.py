from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.api_v1.classes.schemas import ClassCreate, ClassUpdate
from src.api.api_v1.models import Class


async def create_class(session: AsyncSession, class_in: ClassCreate) -> Class:
    class_ = Class(**class_in.model_dump())
    session.add(class_)
    await session.commit()
    return class_


async def get_classes(session: AsyncSession) -> Sequence[Class]:
    stmt = select(Class).order_by(Class.id)
    classes = await session.scalars(stmt)
    return list(classes)


async def get_class_by_id(session: AsyncSession, class_id: int) -> Class | None:
    return await session.get(Class, class_id)


async def get_class_by_num(
    session: AsyncSession,
    class_num: int,
) -> Class | None:
    stmt = (
        select(Class)
        .options(joinedload(Class.teacher))
        .where(Class.class_num == class_num)
    )

    class_: Class | None = await session.scalar(stmt)
    return class_


async def update_class(
    session: AsyncSession,
    class_: Class,
    class_update: ClassUpdate,
) -> Class:
    for class_num, value in class_update.model_dump().items():
        setattr(class_, class_num, value)
    await session.commit()
    return class_


async def delete_class(
    session: AsyncSession,
    class_: Class,
) -> None:
    await session.delete(class_)
    await session.commit()
