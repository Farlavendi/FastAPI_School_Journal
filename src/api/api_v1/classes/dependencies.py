from typing import Annotated

from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .schemas import Class
from core import db_helper
from .crud import get_class_by_id


async def class_by_id(
    class_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Class | None:
    class_ = await get_class_by_id(session=session, class_id=class_id)
    if class_ is not None:
        return class_

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Class with id {class_id} not found",
    )
