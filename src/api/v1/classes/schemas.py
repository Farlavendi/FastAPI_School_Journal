from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from src.api.v1.users.students.schemas import Student
from src.api.v1.users.teachers.schemas import Teacher


class BaseClass(BaseModel):
    class_num: int = Field(..., ge=1)


class ClassCreate(BaseClass):
    id: SkipJsonSchema[UUID] = Field(default_factory=uuid4)
    students: SkipJsonSchema[List[Student]] = Field(default_factory=list)
    teacher: SkipJsonSchema[Teacher] = None


class Class(BaseClass):
    id: UUID = Field()
    students: List[Student]
    teacher: Teacher | None


class ClassResponse(BaseModel):
    id: UUID
    class_num: int
