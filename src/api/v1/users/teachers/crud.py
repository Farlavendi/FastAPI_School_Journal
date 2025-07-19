from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.v1.classes.dependencies import class_id_by_number
from src.api.v1.models import Teacher, Marks
from src.api.v1.models.teachers import SubjectEnum
from src.api.v1.users.marks_schemas import MarksUpdate
from src.api.v1.users.schemas import TeacherUserCreate
from src.auth.utils import hash_password, CurrentUserDep
from src.core.models import User
from src.core.models.users import RoleEnum
from .schemas import TeacherCreate, TeacherUpdate


async def get_teachers(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(
        select(User)
        .where(User.role == RoleEnum.TEACHER)
        .options(joinedload(User.teacher))
        .order_by(User.id)
    )
    teachers = result.scalars().all()
    return teachers


async def create_teacher(
    session: AsyncSession,
    user_in: TeacherUserCreate,
    teacher_in: TeacherCreate,
    subject: SubjectEnum | None
) -> User:
    hashed_password = hash_password(user_in.password)
    user_data = user_in.model_dump(exclude={"password"})

    user = User(**user_data, password=hashed_password)
    session.add(user)
    await session.flush()

    class_id = await class_id_by_number(teacher_in.class_num, session=session)
    teacher_data = teacher_in.model_dump(exclude={"class_id", "class_num", "subject"})
    teacher = Teacher(
        user_id=user.id,
        class_id=class_id,
        subject=subject,
        **teacher_data
    )
    session.add(teacher)

    return user


async def update_teacher(
    session: AsyncSession,
    teacher: TeacherUpdate,
    subject: SubjectEnum,
):
    class_id = await class_id_by_number(teacher.class_num, session=session)
    result = await session.execute(
        update(Teacher)
        .where(Teacher.user_id == teacher.id)
        .values(
            subject=subject,
            class_id=class_id
        )
        .returning(Teacher)
    )
    await session.commit()
    return result.scalar_one()


async def update_marks(
    session: AsyncSession,
    user: CurrentUserDep,
    marks: MarksUpdate
):
    if user.role != RoleEnum.TEACHER:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can edit marks!"
        )
    result = await session.execute(
        update(Marks)
        .where(Marks.student_id == marks.student_id)
        .values(**marks.model_dump(exclude_unset=True))
        .returning(Marks)
    )
    await session.commit()
    return result.scalar_one()
