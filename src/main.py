from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    return "The server is running."


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
