from pydantic import ConfigDict, Field
from pydantic.json_schema import SkipJsonSchema

from src.users.schemas import BaseUser


class BaseStudent(BaseUser):
    model_config = ConfigDict(from_attributes=True)

    class_num: int = Field(..., ge=1)


class StudentCreate(BaseStudent):
    id: SkipJsonSchema[int]


class StudentUpdate(StudentCreate):
    pass


class StudentPartialUpdate(StudentCreate):
    class_num: int | None = None
    username: str | None = None
    email: str | None = None
    password: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None


class Student(BaseStudent):
    pass
