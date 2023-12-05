from fastapi import FastAPI
import uvicorn

from routers import tasks

app = FastAPI()

app.include_router(tasks.router, prefix="/tasks")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
