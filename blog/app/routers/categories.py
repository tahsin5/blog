from fastapi import APIRouter

from blog.services.categories import get,create,update,delete

router = APIRouter()

@router.get("/categories")
async def get_categories():
    pass

@router.post("/categories")
async def create_categories():
    pass

@router.put("/categories")
async def update_categories():
    pass

@router.delete("/categories")
async def delete_categories():
    pass 