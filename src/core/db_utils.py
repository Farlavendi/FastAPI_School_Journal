from asyncio import current_task
from typing import Iterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scope_session(self):
        session = async_scoped_session(
            self.session_factory,
            scope=current_task,
        )
        return session

    async def session_dependency(self) -> Iterator[AsyncSession]:
        async with self.get_scope_session() as session:
            yield session
            await session.remove()


db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=True,
)
