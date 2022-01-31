from fastapi import FastAPI

from blog.services.startup import init_db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup_event():
    try:
        init_db()
    except Exception as e:
        raise Exception("Error with database")