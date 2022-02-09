from fastapi import APIRouter

from blog.services.comments import get,create,update,delete

router = APIRouter()

# Also creates,changes, deletes and retrieves metadata

@router.get("/comments")
async def get_comments():
    pass

@router.post("/comments")
async def create_comments():
    pass

@router.put("/comments")
async def update_comments():
    pass

@router.delete("/comments")
async def delete_comments():
    pass