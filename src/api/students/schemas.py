from pydantic import Field, BaseModel
from pydantic.json_schema import SkipJsonSchema


class BaseStudent(BaseModel):
    user_id: SkipJsonSchema[int] = Field(..., ge=0)
    class_id: int = Field(..., ge=0)


class StudentCreate(BaseStudent):
    pass


class StudentUpdate(StudentCreate):
    id: int


class Student(BaseStudent):
    id: int
