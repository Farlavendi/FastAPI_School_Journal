from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid_utils import UUID

from src.core.models import Base, User

if TYPE_CHECKING:
    from . import Class, Marks


class Student(Base):
    __tablename__ = "students"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="CASCADE",
            name="fk_student_user_id",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    class_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="classes.id",
            ondelete="CASCADE",
            name="fk_student_class_id",
        ),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(back_populates="student")
    class_: Mapped["Class"] = relationship(back_populates="students")
    marks: Mapped["Marks"] = relationship(back_populates="student", cascade="all, delete-orphan")
