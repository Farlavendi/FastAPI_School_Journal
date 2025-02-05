from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base
from src.api.api_v1.models.mixins.int_id_pk import IntIdPkMixin


class User(IntIdPkMixin, Base):
    __abstract__ = True

    email: Mapped[str] = mapped_column(
        unique=True,
    )
    username: Mapped[str] = mapped_column(
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(String(50))
    second_name: Mapped[str | None] = mapped_column(
        String(50), default="", server_default=""
    )
    last_name: Mapped[str] = mapped_column(String(50))

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
