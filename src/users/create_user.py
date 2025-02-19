from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.api_v1.models import Student, Teacher
from api.api_v1.models.users import RoleEnum, User


class UserCreate(BaseModel):
    username: str
    role: RoleEnum
    grade: str = None
    subject: str = None


class UserOut(BaseModel):
    id: int
    username: str
    role: RoleEnum


@app.post("/users/", response_model=UserOut)
async def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    user = User(username=user_create.username, role=user_create.role)
    db.add(user)
    db.commit()
    db.refresh(user)

    if user_create.role == RoleEnum.STUDENT:
        student = Student(user_id=user.id, grade=user_create.grade)
        db.add(student)
    elif user_create.role == RoleEnum.TEACHER:
        teacher = Teacher(user_id=user.id, subject=user_create.subject)
        db.add(teacher)

    db.commit()
    db.refresh(user)

    return user
