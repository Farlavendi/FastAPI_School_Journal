import sqlalchemy
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from . import crud
from .schemas import (
    Teacher,
    TeacherCreate,
    TeacherUpdate,
    TeacherPartialUpdate,
)
from .dependencies import teacher_by_id

teachers_router = APIRouter(tags=["Teachers"])


@teachers_router.get("/", response_model=list[Teacher])
async def get_teachers(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return crud.get_teachers(session)


@teachers_router.get("/{teacher_id}/", response_model=Teacher)
async def get_teacher_by_id(
    teacher: Teacher = Depends(teacher_by_id),
):
    return teacher


@teachers_router.post(
    "/create/",
    response_model=Teacher,
    status_code=status.HTTP_201_CREATED,
)
async def create_teacher(
    teacher_in: TeacherCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        return await crud.create_teacher(session=session, teacher_in=teacher_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Teacher with this username, email or class_id already exists.",
        )


@teachers_router.put("/update/{teacher_id}/")
async def update_teacher(
    teacher_update: TeacherUpdate,
    teacher: Teacher = Depends(teacher_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_teacher(
        session=session,
        teacher=teacher,
        teacher_update=teacher_update,
    )


@teachers_router.patch("/update/{teacher_id}/")
async def update_teacher_partial(
    teacher_update: TeacherPartialUpdate,
    teacher: Teacher = Depends(teacher_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_teacher(
        session=session,
        teacher=teacher,
        teacher_update=teacher_update,
        partial=True,
    )


@teachers_router.delete("/delete/{teacher_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(
    teacher: Teacher = Depends(teacher_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_teacher(
        session=session,
        teacher=teacher,
    )
