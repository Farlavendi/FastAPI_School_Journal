from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from src import certs

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(str(BASE_DIR / ".env"))


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_url: str = getenv("DB_URL")
    db_echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "src" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "src" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


settings = Settings()
