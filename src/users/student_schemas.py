from pydantic import Field, BaseModel


class BaseStudent(BaseModel):
    class_id: int = Field(..., ge=0)


class StudentCreate(BaseStudent):
    pass


class StudentUpdate(StudentCreate):
    id: int


class Student(BaseStudent):
    id: int
