from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from users.model import Base
from core.db_utils import db_helper
from api.views import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router)


@app.get("/")
async def root():
    return "The server is running."


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
