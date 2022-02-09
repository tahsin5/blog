from fastapi import APIRouter

from blog.services.tags import get,create,update,delete

router = APIRouter()

# Also creates,changes, deletes and retrieves metadata

@router.get("/tags")
async def get_tags():
    pass

@router.post("/tags")
async def create_tags():
    pass

@router.put("/tags")
async def update_tags():
    pass

@router.delete("/tags")
async def delete_tags():
    pass