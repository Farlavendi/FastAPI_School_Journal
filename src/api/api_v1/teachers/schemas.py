from pydantic import Field, BaseModel


class BaseTeacher(BaseModel):
    user_id: int = Field(..., ge=0)
    class_id: int = Field(..., ge=0)


class TeacherCreate(BaseTeacher):
    pass


class TeacherUpdate(TeacherCreate):
    id: int


class Teacher(BaseTeacher):
    id: int
