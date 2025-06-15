from fastapi import APIRouter

from src.core.config import settings
from src.users.students.views import students_router
from src.users.teachers.views import teachers_router
from src.users.views import users_router
from .classes.views import classes_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

users_router.include_router(router=students_router)
users_router.include_router(router=teachers_router)

router.include_router(router=classes_router)
router.include_router(router=users_router)
