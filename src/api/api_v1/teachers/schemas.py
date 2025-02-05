from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from src.users.schemas import BaseUser


class BaseTeacher(BaseUser):
    class_id: int = Field(..., ge=1)


class TeacherCreate(BaseTeacher):
    id: SkipJsonSchema[int]


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
    pass
