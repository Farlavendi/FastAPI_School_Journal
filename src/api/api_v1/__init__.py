from fastapi import APIRouter

from users.views import users_router
from .classes.views import classes_router
from .students.views import students_router
from .teachers.views import teachers_router

router = APIRouter()
router.include_router(router=students_router, prefix="/students")
router.include_router(router=classes_router, prefix="/classes")
router.include_router(router=teachers_router, prefix="/teachers")
router.include_router(router=users_router, prefix="/users")
