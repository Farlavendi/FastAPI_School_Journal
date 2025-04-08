import sqlalchemy
from fastapi import APIRouter, HTTPException
from starlette import status

from src.core.db_utils import SessionDep
from . import crud
from .dependencies import ClassByValueDep
from .schemas import (
    Class,
    ClassCreate,
    ClassResponse,
)

classes_router = APIRouter(prefix="/classes", tags=["Classes"])


@classes_router.get("/", response_model=list[ClassResponse])
async def get_classes(
    session: SessionDep,
):
    return await crud.get_classes(session=session)


@classes_router.get("/{value}", response_model=Class)
async def get_class(
    class_: ClassByValueDep,
):
    return class_


@classes_router.post(
    "/create/",
    response_model=Class,
    status_code=status.HTTP_201_CREATED,
)
async def create_class(
    class_in: ClassCreate,
    session: SessionDep,
):
    try:
        return await crud.create_class(session=session, class_in=class_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Class with this number already exists.",
        )


# @classes_router.patch("/update/{class_id}/")
# async def update_class(
#     class_update: ClassUpdate,
#     class_: Class = Depends(class_by_id),
#     session: SessionDep,
# ):
#     return await crud.update_class(
#         session=session,
#         class_=class_,
#         class_update=class_update,
#     )


@classes_router.delete("/delete/{class_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(
    session: SessionDep,
    class_: ClassByValueDep,
):
    return await crud.delete_class(class_=class_, session=session)
