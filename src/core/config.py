from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # db_url: str = getenv("DB_URL")
    db_url: str = "postgresql+asyncpg://postgres@localhost:5432/fastapi_journal"
    db_echo: bool = True  # IMPORTANT set False on production, True is ONLY for debug!


settings = Settings()
