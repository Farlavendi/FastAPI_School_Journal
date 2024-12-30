from os import getenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str = getenv('postgresql+asyncpg://postgres@localhost:5432/school_journal')


settings = Settings()
