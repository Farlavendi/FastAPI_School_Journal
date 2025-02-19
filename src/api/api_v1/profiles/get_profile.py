from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

from api.api_v1.models.users import RoleEnum, User


class UserProfile(BaseModel):
    id: int
    username: str
    role: RoleEnum
    grade: str = None
    subject: str = None


@app.get("/users/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(
        select(User)
        .options(joinedload(User.student), joinedload(User.teacher))
        .filter(User.id == user_id)
    ).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "grade": user.student.grade if user.role == RoleEnum.STUDENT else None,
        "subject": user.teacher.subject if user.role == RoleEnum.TEACHER else None,
    }

    return profile
