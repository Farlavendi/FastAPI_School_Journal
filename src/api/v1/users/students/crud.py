from typing import Sequence
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.v1.auth.utils import hash_password
from src.api.v1.classes.dependencies import class_id_by_number
from src.api.v1.models import Marks, Student
from src.api.v1.users.schemas import StudentUserCreate
from src.core.models import User
from src.core.models.users import RoleEnum
from .schemas import StudentCreate, StudentUpdate


async def get_students(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(
        select(User)
        .where(User.role == RoleEnum.STUDENT)
        .options(joinedload(User.student))
        .order_by(User.id),
    )
    students = result.scalars().all()
    return students


async def get_marks(
    session: AsyncSession,
    student_id: UUID,
):
    result = await session.execute(
        select(Marks)
        .where(Marks.student_id == student_id),
    )
    marks = result.scalar_one_or_none()

    if not marks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Marks not found.',
        )

    return marks


async def create_student(
    session: AsyncSession,
    user_in: StudentUserCreate,
    student_in: StudentCreate,
) -> User:
    hashed_password = hash_password(user_in.password)
    user_data = user_in.model_dump(exclude={"password"})

    user = User(**user_data, password=hashed_password)
    session.add(user)
    await session.flush()

    class_id = await class_id_by_number(student_in.class_num, session=session)
    student_data = student_in.model_dump(exclude={"class_id", "class_num"})
    student = Student(user_id=user.id, class_id=class_id, **student_data)
    session.add(student)
    await session.flush()

    marks = Marks(student_id=student.id)
    session.add(marks)

    return user


async def update_student(
    session: AsyncSession,
    student: StudentUpdate,
):
    class_id = await class_id_by_number(student.class_num, session=session)
    result = await session.execute(
        update(Student)
        .where(Student.user_id == student.id)
        .values(
            id=student.id,
            class_id=class_id,
        )
        .returning(Student),
    )
    await session.commit()
    return result.scalar_one()
