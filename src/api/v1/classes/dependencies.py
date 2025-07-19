from typing import Annotated

from fastapi import Depends, HTTPException, Path
from sqlalchemy import select
from starlette import status

from src.api.v1.models import Class
from src.core.db_utils import SessionDep
from . import schemas
from .crud import get_class


async def class_by_id(
    value: Annotated[int, Path],
    session: SessionDep,
    by_id: Annotated[bool, Path] = False,
) -> Class | None:
    return await get_class(session=session, value=value, by_id=by_id)


async def class_id_by_number(
    class_num: Annotated[int, Path],
    session: SessionDep,
) -> int:
    result = await session.execute(
        select(Class.id)
        .where(Class.class_num == class_num),
    )
    class_id = result.scalar_one_or_none()

    if class_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found.",
        )

    return class_id


ClassByValueDep = Annotated[schemas.Class, Depends(class_by_id)]
ClassIdByNumberDep = Annotated[schemas.Class, Depends(class_id_by_number)]
