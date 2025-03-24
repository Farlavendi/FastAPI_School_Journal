from pydantic import Field, BaseModel


class BaseStudent(BaseModel):
    class_id: int = Field(..., ge=0)


class StudentCreate(BaseStudent):
    pass


class StudentUpdate(StudentCreate):
    id: int


class Student(BaseStudent):
    id: int


class StudentResponse(BaseModel):
    id: int
    user_id: int
    class_id: int


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    password: str
    first_name: str
    second_name: str
    last_name: str
    role: str
    student: StudentResponse