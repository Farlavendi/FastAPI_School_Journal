from pydantic import BaseModel, ConfigDict, Field


class BaseClass(BaseModel):
    class_num: int = Field(..., ge=1)


class ClassCreate(BaseClass):
    pass


class ClassUpdate(ClassCreate):
    pass


class Class(BaseClass):
    model_config = ConfigDict(from_attributes=True)

    id: int
