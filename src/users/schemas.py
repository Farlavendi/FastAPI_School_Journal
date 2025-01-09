from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    hashed_password: str
    first_name: str | None
    second_name: str | None
    last_name: str | None

    class Config:
        orm_mode = True
