from typing import Annotated

from fastapi import Path, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core import db_helper
from .crud import get_class_by_id
from .schemas import Class


async def class_by_id(
    class_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Class:
    class_ = await get_class_by_id(session=session, class_id=class_id)
    if class_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with id {class_id} not found",
        )
    return class_

async def class_id_by_number(
    class_num: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> int | None:
    result = await session.execute(
        select(Class.id).filter(Class.class_num == class_num)
    )
    class_id = result.scalar_one_or_none()

    if class_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found."
        )

    return class_id
