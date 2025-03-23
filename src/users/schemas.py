from pydantic import BaseModel, EmailStr, ConfigDict, Field
from pydantic.json_schema import SkipJsonSchema

from src.api.models.users import RoleEnum


class BaseUser(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(...)
    first_name: str = Field(..., min_length=1, max_length=100)
    second_name: str | None = Field(max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: RoleEnum


class UserSchemaForAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    # id: int = Field(ge=1)
    email: EmailStr = Field(...)
    username: str = Field(..., min_length=3, max_length=50)
    hashed_password: SkipJsonSchema[bytes] = Field(...)
    first_name: str | None = Field(..., min_length=1, max_length=100)
    second_name: str | None = Field(max_length=100)
    last_name: str | None = Field(..., min_length=1, max_length=100)
    is_active: SkipJsonSchema[bool] = True
    role: RoleEnum


class UserCreate(BaseUser):
    password: str


class StudentUserCreate(BaseUser):
    role: SkipJsonSchema[RoleEnum] = RoleEnum.STUDENT


class TeacherUserCreate(BaseUser):
    role: SkipJsonSchema[RoleEnum] = RoleEnum.TEACHER


class User(BaseUser):
    id: int
