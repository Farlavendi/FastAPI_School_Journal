from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    hashed_password: str
    first_name: str | None
    second_name: str | None
    last_name: str | None
