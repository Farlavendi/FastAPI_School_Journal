from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.classes.dependencies import class_id_by_number
from src.api.models import User, Student
from src.api.models.users import RoleEnum
from src.auth.utils import hash_password
from src.users.schemas import StudentUserCreate
from src.users.students.schemas import StudentCreate


async def get_students(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(
        select(User)
        .filter(User.role == RoleEnum.STUDENT)
        .options(joinedload(User.student))
        .order_by(User.id)
    )
    students = result.scalars().all()
    return students


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

    return user
