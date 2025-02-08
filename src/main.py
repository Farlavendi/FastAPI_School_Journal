from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, ORJSONResponse

from api.api_v1 import router as api_router
from auth.views import auth_router
from core.config import settings
from core.db_utils import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    uvicorn.run("main:app", reload=True)
