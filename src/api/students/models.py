from sqlalchemy.orm import Mapped

from users.models import UserModel


class Student(UserModel):
    __tablename__ = "students"

    class_num: Mapped[int]
