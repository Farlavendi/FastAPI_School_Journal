from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )


class UserModel(Base):
    __abstract__ = True

    email: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )
    first_name: Mapped[str]
    second_name: Mapped[str]
    last_name: Mapped[str]
