from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from api.api_v1.models.users import RoleEnum
from users.schemas import BaseUser


class BaseTeacher(BaseUser):
    class_id: int = Field(..., ge=0)


class TeacherCreate(BaseTeacher):
    role: SkipJsonSchema[RoleEnum] = 'teacher'


class TeacherUpdate(TeacherCreate):
    pass


class TeacherPartialUpdate(TeacherCreate):
    class_id: int | None = None
    username: str | None = None
    email: str | None = None
    hashed_password: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None


class Teacher(BaseTeacher):
    id: int
    role: SkipJsonSchema[RoleEnum] = RoleEnum.TEACHER
