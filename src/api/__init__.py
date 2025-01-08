from fastapi import APIRouter
from .students.views import students_router
from .classes.views import classes_router

router = APIRouter()
router.include_router(router=students_router, prefix="/students")
router.include_router(router=classes_router, prefix="/classes")
