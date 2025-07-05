from typing import Optional

from pydantic import Field, BaseModel
from pydantic.json_schema import SkipJsonSchema


class BaseStudent(BaseModel):
    class_id: int = Field(..., ge=0)


class StudentCreate(BaseStudent):
    class_id: SkipJsonSchema[int] = None
    class_num: int


class StudentUpdate(BaseModel):
    id: int
    class_num: Optional[int] = None


class Student(BaseStudent):
    id: int


class StudentResponse(BaseModel):
    id: int
    user_id: int
    class_id: int


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    password: str
    first_name: str
    second_name: str
    last_name: str
    role: str
    student: StudentResponse
