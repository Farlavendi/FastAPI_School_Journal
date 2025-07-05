from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from src.api.v1.users.students.schemas import Student
from src.api.v1.users.teachers.schemas import Teacher


class ClassCreate(BaseModel):
    class_num: int = Field(..., ge=1)
    students: SkipJsonSchema[Optional[List[Student]]] = []
    teacher: SkipJsonSchema[Optional[Teacher]] = None


class Class(ClassCreate):
    # id: UUID = Field(default_factory=uuid7)
    id: int = Field(..., ge=0)
    students: Optional[List[Student]]
    teacher: Optional[Teacher]


class ClassResponse(BaseModel):
    id: int
    class_num: int
