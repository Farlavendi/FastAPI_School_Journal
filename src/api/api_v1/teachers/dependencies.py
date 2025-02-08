from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from . import crud


async def teacher_by_id(
    teacher_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    teacher = await crud.get_teacher_by_id(session=session, teacher_id=teacher_id)
    if teacher:
        return teacher

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Teacher with id {teacher_id} not found.",
    )