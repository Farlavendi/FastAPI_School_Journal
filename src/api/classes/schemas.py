from pydantic import BaseModel, Field


class ClassCreate(BaseModel):
    class_num: int = Field(..., ge=1)


class Class(ClassCreate):
    id: int = Field(..., ge=0)
