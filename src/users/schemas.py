from fastapi import Path
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr = Field(...)
    username: str = Field(..., min_length=3, max_length=50)
    hashed_password: str
    first_name: str | None = Field(...)
    second_name: str | None = Field()
    last_name: str | None = Field(...)


class UserCreate(BaseUser):
    pass


class User(BaseUser):
    id: int = Field(ge=1, exclude=True)
