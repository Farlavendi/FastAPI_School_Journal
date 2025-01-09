from pydantic import ConfigDict

from users.schemas import User


class BaseStudent(User):
    class_num: int


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

    id: int

    class Config:
        orm_mode = True