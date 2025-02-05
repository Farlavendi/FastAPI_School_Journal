from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import SkipJsonSchema


class BaseClass(BaseModel):
    class_num: int = Field(..., ge=1)


class ClassCreate(BaseClass):
    pass


class ClassUpdate(ClassCreate):
    pass


class Class(BaseClass):

    id: int = Field(ge=1)
