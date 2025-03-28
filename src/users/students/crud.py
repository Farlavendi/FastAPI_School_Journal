from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.models import User, Student
from src.api.models.users import RoleEnum
from src.auth.utils import hash_password
from src.users.schemas import StudentUserCreate
from src.users.students.schemas import StudentCreate


async def get_students(session: AsyncSession) -> Sequence[User]:
    stmt = (
        select(User)
        .filter(User.role == RoleEnum.STUDENT)
        .options(joinedload(User.student))
        .order_by(User.id)
    )
    result = await session.execute(stmt)
    students = result.scalars().all()
    return students


async def create_student(
    session: AsyncSession,
    user_in: StudentUserCreate,
    student_in: StudentCreate
) -> User:
    hashed_password = hash_password(user_in.password)
    user_data = user_in.model_dump(exclude={"password"})
    
    user = User(**user_data, password=hashed_password)
    session.add(user)
    await session.flush()

    student = Student(user_id=user.id, **student_in.model_dump())
    session.add(student)

    return user
