from pydantic import Field, BaseModel


class BaseTeacher(BaseModel):
    class_id: int = Field(..., ge=0)


class TeacherCreate(BaseTeacher):
    pass


class TeacherUpdate(TeacherCreate):
    id: int


class Teacher(BaseTeacher):
    id: int


class TeacherResponse(BaseModel):
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
    teacher: TeacherResponse