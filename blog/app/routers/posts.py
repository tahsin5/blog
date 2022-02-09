from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, AnyUrl

from blog.services.posts import get,create,update,delete


class PostModel(BaseModel):
    
    title: str
    published_at: Optional[str]
    images: Optional[str]
    content: Optional[str]
    links: Optional[AnyUrl]

router = APIRouter()

# Also creates,changes, deletes and retrieves metadata

@router.get("/posts")
async def get_posts():
    pass

@router.post("/posts")
async def create_posts():
    pass

@router.put("/posts")
async def update_posts():
    pass

@router.delete("/posts")
async def delete_posts():
    pass