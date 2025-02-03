from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import SkipJsonSchema


class BaseClass(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(ge=1)
    class_num: int = Field(..., ge=1)


class ClassCreate(BaseClass):
    id: SkipJsonSchema[int]


class ClassUpdate(ClassCreate):
    pass


class Class(BaseClass):
    pass
