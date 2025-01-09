from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from users.models import UserModel


class Student(UserModel):
    __tablename__ = "students"

    class_num: Mapped[int]
