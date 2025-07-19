from typing import List

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema
from pydantic.types import UUID
from uuid_utils import uuid4

from src.api.v1.users.students.schemas import Student
from src.api.v1.users.teachers.schemas import Teacher


class BaseClass(BaseModel):
    class_num: int = Field(...)


class ClassCreate(BaseModel):
    id: SkipJsonSchema[UUID] = Field(default_factory=uuid4)
    class_num: int = Field(..., ge=1)
    students: SkipJsonSchema[List[Student]] = Field(default_factory=list)
    teacher: SkipJsonSchema[Teacher] = None


class Class(BaseClass):
    id: UUID = Field()
    students: List[Student]
    teacher: Teacher | None


class ClassResponse(BaseModel):
    id: UUID
    class_num: int
