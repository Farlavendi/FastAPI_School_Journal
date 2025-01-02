from sqlalchemy import Integer, String

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __abstract__ = True
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    email: Mapped[String] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    second_name: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    last_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
