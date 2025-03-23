from api.models.users import RoleEnum, User
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from .get_profile import UserProfile


class UserProfileUpdate(BaseModel):
    username: str = None
    grade: str = None  # For students
    subject: str = None  # For teachers


@app.patch("/users/{user_id}/profile", response_model=UserProfile)
async def update_user_profile(
    user_id: int, profile_update: UserProfileUpdate, db: Session = Depends(get_db)
):
    user = db.execute(select(User).filter(User.id == user_id)).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if profile_update.username:
        user.username = profile_update.username

    if user.role == RoleEnum.STUDENT and profile_update.grade:
        user.student.grade = profile_update.grade
    elif user.role == RoleEnum.TEACHER and profile_update.subject:
        user.teacher.subject = profile_update.subject

    db.commit()
    db.refresh(user)

    profile = {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "grade": user.student.grade if user.role == RoleEnum.STUDENT else None,
        "subject": user.teacher.subject if user.role == RoleEnum.TEACHER else None,
    }

    return profile
