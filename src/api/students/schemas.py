from pydantic import ConfigDict, Field

from src.users.schemas import BaseUser


class BaseStudent(BaseUser):
    class_num: int = Field(..., ge=1)


class StudentCreate(BaseStudent):
    pass


class StudentUpdate(StudentCreate):
    pass


class StudentPartialUpdate(StudentCreate):
    class_num: int | None = None
    username: str | None = None
    email: str | None = None
    hashed_password: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None


class Student(BaseStudent):
    model_config = ConfigDict(from_attributes=True)
