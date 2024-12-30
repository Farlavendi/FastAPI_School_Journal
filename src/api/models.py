from typing import Annotated

from fastapi import Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column

from users.model import Base, User


# class Class(BaseModel):
#     id: Annotated[int, Field(ge=0)]
#     number: Annotated[int, Field(gt=0)]


# class __tudent(User):
#     id: Annotated[int, Field(ge=0)]
#     class_num: Annotated[int, Field(ge=1), Path(alias="Class number")]


class Class(Base):
    __tablename__ = "classes"
    id: Mapped[int] = mapped_column(primary_key=True)
    class_num: Mapped[int] = mapped_column(alias="Class number")


class Student(User):
    id: Mapped[int] = mapped_column(primary_key=True)
    class_num: Mapped[int] = mapped_column(alias="Class number")
