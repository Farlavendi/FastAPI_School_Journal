from pydantic import BaseModel, ConfigDict


class BaseClass(BaseModel):
    __tablename__ = "classes"
    class_num: int


class ClassCreate(BaseClass):
    pass


class ClassUpdate(ClassCreate):
    pass


class Class(BaseClass):
    model_config = ConfigDict(from_attributes=True)

    id: int
