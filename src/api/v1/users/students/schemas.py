from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema


class BaseStudent(BaseModel):
    class_id: UUID = Field(...)


class StudentCreate(BaseStudent):
    class_id: SkipJsonSchema[UUID] = Field(default_factory=uuid4)
    class_num: int = Field(..., ge=1)


class StudentUpdate(BaseModel):
    id: UUID = Field(...)
    class_num: int | None = Field(None, ge=1)


class Student(BaseStudent):
    id: UUID


class StudentResponse(BaseModel):
    id: UUID
    user_id: UUID
    class_id: UUID


class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    password: str
    first_name: str
    second_name: str
    last_name: str
    role: str
    student: StudentResponse
