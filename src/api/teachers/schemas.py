from pydantic import ConfigDict, Field

from src.users.schemas import BaseUser


class BaseTeacher(BaseUser):
    class_id: int = Field(..., ge=1)


class TeacherCreate(BaseTeacher):
    pass


class TeacherUpdate(BaseTeacher):
    pass


class TeacherPartialUpdate(BaseTeacher):
    class_id: int | None = None
    username: str | None = None
    email: str | None = None
    hashed_password: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None


class Teacher(BaseTeacher):
    model_config = ConfigDict(from_attributes=True)

    id: int
