from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic.json_schema import SkipJsonSchema

from src.api.models.users import RoleEnum
from .students.schemas import Student
from .teachers.schemas import Teacher


class BaseUser(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(...)
    first_name: str = Field(..., min_length=1, max_length=100)
    second_name: str | None = Field(max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: RoleEnum



# class UserSchemaForAuth(BaseUser):
#     model_config = ConfigDict(from_attributes=True, strict=True)
#     id: int
#     # hashed_password: SkipJsonSchema[str] = Field(...)
#     is_active: SkipJsonSchema[bool] = True


class UserCreate(BaseUser):
    password: str


class StudentUserCreate(BaseUser):
    role: SkipJsonSchema[RoleEnum] = RoleEnum.STUDENT


class TeacherUserCreate(BaseUser):
    role: SkipJsonSchema[RoleEnum] = RoleEnum.TEACHER


class User(BaseUser):
    id: int
    is_active: bool
    student: Optional[Student]
    teacher: Optional[Teacher]
