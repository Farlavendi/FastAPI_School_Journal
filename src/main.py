from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, ORJSONResponse
from sqlalchemy import event

from api.api_v1 import router as api_router
from api.api_v1.models import User
from auth.views import auth_router
from core.config import settings
from core.db_utils import db_helper
from core.events import create_student_or_teacher, create_profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    event.listen(User, 'after_insert', create_student_or_teacher)
    event.listen(User, 'after_insert', create_profile)

    yield
    await db_helper.dispose()



app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
app.include_router(router=api_router, prefix=settings.api_v1_prefix)
app.include_router(router=auth_router)


@app.get("/")
async def root_and_redirect():
    redirect_url = RedirectResponse("/docs")
    return redirect_url


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
