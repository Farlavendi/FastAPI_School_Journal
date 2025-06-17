from typing import Optional, List

from pydantic import BaseModel, Field

from src.api.v1.users.students.schemas import Student
from src.api.v1.users.teachers.schemas import Teacher


class ClassCreate(BaseModel):
    class_num: int = Field(..., ge=1)


class Class(ClassCreate):
    id: int = Field(..., ge=0)
    students: Optional[List[Student]]
    teacher: Optional[Teacher]


class ClassResponse(BaseModel):
    id: int
    class_num: int
