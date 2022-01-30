from fastapi import FastAPI

from blog.services.startup import init_db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup_event():
    init_db()
    pass