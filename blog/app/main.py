from fastapi import FastAPI, HTTPException

from blog.services.startup import init_db
from blog.app.routers import posts, tags, categories, comments

# TODO: Add custom exception handling through fastapi

app = FastAPI()
app.include_router(posts.router)
app.include_router(tags.router)
app.include_router(posts.router)
app.include_router(posts.router)

@app.on_event("startup")
async def startup_event():
    
    result, error_str = init_db()
    if not result:
        raise HTTPException(status_code=500, 
                        detail=error_str)

@app.get("/")
async def root():
    return {"message": "Blog backend API"}