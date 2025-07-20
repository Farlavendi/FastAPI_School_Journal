from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from src.api.v1.models.teachers import SubjectEnum


class BaseTeacher(BaseModel):
    class_id: UUID = Field(...)
    subject: SubjectEnum | None = None


class TeacherCreate(BaseTeacher):
    class_id: SkipJsonSchema[UUID] = Field(default_factory=uuid4)
    class_num: int = Field(..., ge=1)
    subject: SkipJsonSchema[SubjectEnum] = None


class TeacherUpdate(BaseModel):
    id: UUID = Field(...)
    class_num: int | None = Field(None, ge=1)


class Teacher(BaseTeacher):
    id: UUID


class TeacherResponse(BaseModel):
    id: UUID
    user_id: UUID
    class_id: UUID
    subject: SubjectEnum | None


class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    password: str
    first_name: str
    second_name: str
    last_name: str
    role: str
    teacher: TeacherResponse
