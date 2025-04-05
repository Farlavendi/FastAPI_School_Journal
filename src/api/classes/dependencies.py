from typing import Annotated

from fastapi import Path, HTTPException
from sqlalchemy import select
from starlette import status

from src.api.models import Class
from src.core.db_utils import SessionDep
from .crud import get_class


async def class_by_id(
    value: Annotated[int, Path],
    by_id: Annotated[bool, Path],
    session: SessionDep,
):
    return await get_class(session=session, value=value, by_id=by_id)


async def class_id_by_number(
    class_num: Annotated[int, Path],
    session: SessionDep,
) -> int:
    result = await session.execute(
        select(Class.id)
        .filter(Class.class_num == class_num)
    )
    class_id = result.scalar_one_or_none()

    if class_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found."
        )

    return class_id
