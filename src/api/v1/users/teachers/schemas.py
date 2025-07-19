from pydantic import Field, BaseModel
from pydantic.json_schema import SkipJsonSchema

from src.api.v1.models.teachers import SubjectEnum


class BaseTeacher(BaseModel):
    class_id: int = Field(..., ge=0)
    subject: SubjectEnum | None = None


class TeacherCreate(BaseTeacher):
    class_id: SkipJsonSchema[int] = None
    class_num: int
    subject: SkipJsonSchema[SubjectEnum] = None


class TeacherUpdate(BaseModel):
    id: int = Field(..., ge=0)
    class_num: int | None = None


class Teacher(BaseTeacher):
    id: int


class TeacherResponse(BaseModel):
    id: int
    user_id: int
    class_id: int
    subject: SubjectEnum | None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    password: str
    first_name: str
    second_name: str
    last_name: str
    role: str
    teacher: TeacherResponse
