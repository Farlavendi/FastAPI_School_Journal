import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import db_helper
from src.users.schemas import TeacherUserCreate
from src.users.teachers import crud
from src.users.teachers.crud import create_teacher
from src.users.teachers.schemas import TeacherCreate, UserResponse

teachers_router = APIRouter(prefix="/teachers")


@teachers_router.get("/get-teachers", response_model=list[UserResponse])
async def get_teachers(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_teachers(session=session)


@teachers_router.post("/create-teacher")
async def create_user_teacher(
    user_in: TeacherUserCreate,
    teacher_in: TeacherCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        user = await create_teacher(session=session, user_in=user_in, teacher_in=teacher_in)
        await session.commit()
        return user
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating user.")
