from pydantic import Field, BaseModel
from pydantic.json_schema import SkipJsonSchema

from src.api.api_v1.models.users import RoleEnum
from src.users.schemas import BaseUser


class BaseStudent(BaseModel):
    user_id: int = Field(..., ge=0)
    class_id: int = Field(..., ge=0)


class StudentCreate(BaseStudent):
    pass


class StudentUpdate(StudentCreate):
    id: int


class Student(BaseStudent):
    id: int
