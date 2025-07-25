import re
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic.json_schema import SkipJsonSchema

from src.core.models.users import RoleEnum
from .students.schemas import Student
from .teachers.schemas import Teacher

password_regex = r"^[a-zA-Z0-9_]+$"


class BaseUser(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=20, pattern=password_regex)
    first_name: str = Field(..., min_length=1, max_length=100)
    second_name: str | None = Field(max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: RoleEnum

    @field_validator("password", mode="plain")
    @classmethod
    def validate_password(cls, password: str):
        if len(password) < 8 or len(password) > 20:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must contain between 8 and 20 characters.",
            )
        if not re.match(password_regex, password):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password can only contain letters, digits or _ sign.",
            )

        return password


class StudentUserCreate(BaseUser):
    role: SkipJsonSchema[RoleEnum] = RoleEnum.STUDENT


class TeacherUserCreate(BaseUser):
    role: SkipJsonSchema[RoleEnum] = RoleEnum.TEACHER


class User(BaseModel):
    id: UUID = Field(...)
    email: EmailStr
    username: str
    password: str
    first_name: str
    second_name: str
    last_name: str
    role: RoleEnum
    is_active: bool
    is_superuser: bool
    is_verified: bool
    student: Student | None
    teacher: Teacher | None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None
