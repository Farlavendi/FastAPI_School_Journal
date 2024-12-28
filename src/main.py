import uvicorn
from fastapi import FastAPI

from api.views import api_router

app = FastAPI()

app.include_router(router=api_router)


@app.get("/")
async def root():
    return "The server is running."

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)