import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core import db_helper
from . import crud
from .dependencies import class_by_id
from .schemas import (
    Class,
    ClassCreate,
    ClassResponse,
)

classes_router = APIRouter(prefix="/classes", tags=["Classes"])


@classes_router.get("/", response_model=list[ClassResponse])
async def get_classes(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_classes(session=session)


@classes_router.get("/{value}", response_model=Class)
async def get_class(
    class_: Class = Depends(class_by_id),
):
    return class_


@classes_router.post(
    "/create/",
    response_model=Class,
    status_code=status.HTTP_201_CREATED,
)
async def create_class(
    class_in: ClassCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        return await crud.create_class(session=session, class_in=class_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Class with this number already exists.",
        )


# @classes_router.put("/update/{class_id}/")
# async def update_class(
#     class_update: ClassUpdate,
#     class_: Class = Depends(class_by_id),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     return await crud.update_class(
#         session=session,
#         class_=class_,
#         class_update=class_update,
#     )


@classes_router.delete("/delete/{class_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(
    class_: Class = Depends(class_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_class(class_=class_, session=session)
