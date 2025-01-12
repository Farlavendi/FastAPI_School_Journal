from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(str(BASE_DIR / ".env"))


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_url: str = getenv("DB_URL")
    db_echo: bool = False  # IMPORTANT set False on production, True is ONLY for debug!


settings = Settings()
