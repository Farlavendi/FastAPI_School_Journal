from pydantic import BaseModel, EmailStr


class Class(BaseModel):
    id: int
    number: int

class Student(BaseModel):
    id: int
    email: EmailStr