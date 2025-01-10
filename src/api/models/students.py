from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .users import UserModel


class Student(UserModel):
    __tablename__ = "students"

    class_num: Mapped[int] = mapped_column(
        ForeignKey("classes.class_num", name="fk_student_class_num"),
    )
