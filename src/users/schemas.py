import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic.json_schema import SkipJsonSchema

from src.api.models.users import RoleEnum
from .students.schemas import Student
from .teachers.schemas import Teacher

password_regex = r'^[A-Za-z0-9_]+$'


class BaseUser(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(...)
    first_name: str = Field(..., min_length=1, max_length=100)
    second_name: str | None = Field(max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: RoleEnum


    @field_validator("password", mode="after")
    @classmethod
    def validate_password(cls, password: str):
        if len(password) < 8 or len(password) > 20:
            raise ValueError("Password must contain between 8 and 20 characters.")

        if not re.match(password_regex, password):
            raise ValueError("Password can only contain letters and digits.")

        return password

class StudentUserCreate(BaseUser):
    role: SkipJsonSchema[RoleEnum] = RoleEnum.STUDENT


class TeacherUserCreate(BaseUser):
    role: SkipJsonSchema[RoleEnum] = RoleEnum.TEACHER


class User(BaseUser):
    id: int
    is_active: bool
    student: Optional[Student]
    teacher: Optional[Teacher]
