from fastapi import Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PostCreate ,PostResponse
from app.token import verify_access_token
from app.db_models import Post


router = APIRouter(
    tags=["Post"]
)   

@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(verify_access_token)):
    new_post = Post(
        title=post.title,
        content=post.content,
        owner_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/posts/my_posts", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(verify_access_token)):
    posts = db.query(Post).filter(Post.owner_id == current_user.id).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post(s) Not Found")
    return posts

@router.get("/posts", response_model=list[PostResponse])
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(verify_access_token)):
    posts = db.query(Post).all()
    return posts

@router.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(verify_access_token)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(verify_access_token)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    
    db.delete(db_post)
    db.commit()
    return None