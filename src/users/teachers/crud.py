from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.classes.dependencies import class_id_by_number
from src.api.models import User, Teacher
from src.api.models.teachers import SubjectEnum
from src.api.models.users import RoleEnum
from src.auth.utils import hash_password
from src.users.schemas import TeacherUserCreate
from src.users.teachers.schemas import TeacherCreate


async def get_teachers(session: AsyncSession) -> Sequence[User]:
    stmt = (
        select(User)
        .filter(User.role == RoleEnum.TEACHER)
        .options(joinedload(User.teacher))
        .order_by(User.id)
    )
    result = await session.execute(stmt)
    teachers = result.scalars().all()
    return teachers


async def create_teacher(
    session: AsyncSession,
    user_in: TeacherUserCreate,
    teacher_in: TeacherCreate,
    subject: SubjectEnum
) -> User:
    hashed_password = hash_password(user_in.password)
    user_data = user_in.model_dump(exclude={"password"})

    user = User(**user_data, password=hashed_password)
    session.add(user)
    await session.flush()

    class_id = await class_id_by_number(teacher_in.class_num, session=session)
    teacher_data = teacher_in.model_dump(exclude={"class_id", "class_num", "subject"})
    teacher = Teacher(user_id=user.id, class_id=class_id, subject=subject ,**teacher_data)
    session.add(teacher)

    return user