from enum import Enum
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid_utils import UUID

from src.core.models import Base, User

if TYPE_CHECKING:
    from . import Class


class SubjectEnum(Enum):
    MATH = "MATH"
    ENGLISH = "ENGLISH"
    PHYSICS = "PHYSICS"
    CHEMISTRY = "CHEMISTRY"
    HISTORY = "HISTORY"
    GEOGRAPHY = "GEOGRAPHY"
    LITERATURE = "LITERATURE"


class Teacher(Base):
    __tablename__ = "teachers"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="CASCADE",
            name="fk_teacher_user_id",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    class_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="classes.id",
            ondelete="CASCADE",
            name="fk_teacher_class_id",
        ),
        nullable=False,
        unique=True,
        index=True,
    )
    subject: Mapped[SubjectEnum] = mapped_column(
        sa.Enum(SubjectEnum, name='subject_enum'), nullable=True, index=True,
    )

    user: Mapped["User"] = relationship(back_populates="teacher")
    class_: Mapped["Class"] = relationship(back_populates="teacher", single_parent=True)
