from pydantic import BaseModel
from sqlalchemy.orm import Mapped


class Class(BaseModel):
    __tablename__ = "classes"

    class_num: Mapped[int]
