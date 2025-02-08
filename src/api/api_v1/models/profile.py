from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from . import Base

if TYPE_CHECKING:
    from . import User


class Profile(Base):
    __tablename__ = "profiles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
            name="fk_profile_user_id",
        ),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="profile")

    __table_args__ = (UniqueConstraint("user_id"),)
