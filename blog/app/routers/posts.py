from typing import Optional
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, AnyUrl

from blog.services.posts import PostService


class Post(BaseModel):
    
    title: str
    published_at:  Optional[str] = None
    content: str
    image_contents: Optional[str] = None  # Base64 encoded
    links: Optional[AnyUrl] = None,
    metadata_key: Optional[str] = None,
    metadata_content: Optional[str] = None

router = APIRouter()

# Also creates,changes, deletes and retrieves metadata

@router.get("/posts")
async def get_posts():
    # get(post) 
    return {"message": "Good to go"}

@router.post("/posts")
async def create_posts(
    post: Post,
    service: PostService = Depends(PostService)
):
    
    result, response_msg = service.create(post)
    if result:
        return_obj = {"status": "success", "message": response_msg}
        return JSONResponse(status_code=status.HTTP_201_CREATED, 
                            content=return_obj)
    else:
        return_obj = {"status": "error", "message": response_msg}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            content=return_obj)



@router.put("/posts")
async def update_posts():
    pass

@router.delete("/posts")
async def delete_posts():
    pass