from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import Annotated, List
from api.models import Post, User
from api.schemas.posts import PostCreate, PostResponse
from core.deps import get_db
from api.auth.authentication import get_current_active_user
# from api.auth import user_dependency


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


user_dependency = Annotated[dict, Depends(get_current_active_user)]

@router.post("/posts/post", response_model=None)
async def create_post(user: user_dependency, post: PostCreate, db:Session = Depends(get_db)):
    new_post = Post(content=post.content, user_id=post.user_id)
    db.add(new_post)
    db.commit()
    return {"post": post}


@router.get("/posts", response_model=List[PostResponse])
async def read_posts(user: user_dependency, db:Session=Depends(get_db)):
    posts = db.query(Post,).all()

    # query = db.query(User).join(User.posts,(User.id == Post.user_id))  
    # results = query.all() 
    
    return posts


