from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.models import Profile
from api.api_v1.models.students import Student
from api.api_v1.models.teachers import Teacher
from api.api_v1.models.users import RoleEnum


def create_student_or_teacher(mapper, connection, target):

    session = AsyncSession.object_session(target)
    if target.role == RoleEnum.STUDENT:
        student = Student(id=target.id)
        session.add(student)
        session.commit()
    elif target.role == RoleEnum.TEACHER:
        teacher = Teacher(id=target.id)
        session.add(teacher)
        session.commit()


def create_profile(mapper, connection, target):
    session = AsyncSession.object_session(target)
    profile = Profile(id=target.id)
    session.add(profile)
    session.commit()
