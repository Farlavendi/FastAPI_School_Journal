from pydantic import BaseModel


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"

class TokenData(BaseModel):
    username: str | None = None
