from typing import Annotated

from fastapi import Path
from pydantic import BaseModel, Field

from users.models import User

class Class(BaseModel):
    id: Annotated[int, Field(ge=0)]
    number: Annotated[int, Field(gt=0)]


class Student(User):
    id: Annotated[int, Field(ge=0)]
    class_num: Annotated[int, Field(ge=1), Path(alias="Class number")]
