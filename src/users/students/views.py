import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import db_helper
from src.users.schemas import StudentUserCreate
from src.users.students import crud
from src.users.students.crud import create_student
from src.users.students.schemas import StudentCreate, UserResponse

students_router = APIRouter(prefix="/students")


@students_router.get("/get-students", response_model=list[UserResponse])
async def get_students(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_students(session=session)


@students_router.post("/create-student")
async def create_user_student(
    user_in: StudentUserCreate,
    student_in: StudentCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        user = await create_student(session=session, user_in=user_in, student_in=student_in)
        await session.commit()
        return user
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating user.")