from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Path, status

from src.core.db_utils import SessionDep
from src.core.models import User
from . import crud, schemas


async def user_by_id(
    user_id: Annotated[UUID, Path],
    session: SessionDep,
) -> User:
    user = await crud.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    return user


UserByIdDep = Annotated[schemas.User, Depends(user_by_id)]
