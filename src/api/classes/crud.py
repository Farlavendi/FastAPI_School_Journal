from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.classes.schemas import *


async def create_class(session: AsyncSession, class_in: ClassCreate) -> Class:
    class_ = Class(**class_in.model_dump())
    session.add(class_)
    await session.commit()
    return class_


async def get_classes(session: AsyncSession) -> list[Class]:
    stmt = select(Class)
    result: Result = await session.execute(stmt)
    classes = result.scalars().all()
    return list(classes)


async def get_class_by_id(session: AsyncSession, class_id: int) -> Class | None:
    return await session.get(Class, class_id)


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
):
    await session.delete(class_)
    await session.commit()
