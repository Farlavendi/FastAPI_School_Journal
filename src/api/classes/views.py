from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core import db_helper
from . import crud
from .dependencies import class_by_id
from .schemas import *

classes_router = APIRouter(tags=["Classes"])


@classes_router.get("/", response_model=list[Class])
async def get_classes(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_classes(session=session)


@classes_router.get("/{class_id}", response_model=Class)
async def get_class_by_id(
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
    return await crud.create_class(session=session, class_in=class_in)


@classes_router.put("/update/{class_id}/")
async def update_class(
    class_update: ClassUpdate,
    class_: Class = Depends(class_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_class(
        session=session,
        class_=class_,
        class_update=class_update,
    )


@classes_router.delete("/remove/{class_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_class(
    class_: Class,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_class(class_=class_, session=session)
