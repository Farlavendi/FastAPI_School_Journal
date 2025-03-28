from pydantic import Field, BaseModel
from pydantic.json_schema import SkipJsonSchema


class BaseTeacher(BaseModel):
    class_id: int = Field(..., ge=0)


class TeacherCreate(BaseTeacher):
    class_id: SkipJsonSchema[int] = None
    class_num: int


class TeacherUpdate(TeacherCreate):
    id: int


class Teacher(BaseTeacher):
    id: int


class TeacherResponse(BaseModel):
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
    teacher: TeacherResponse