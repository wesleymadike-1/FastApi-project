from fastapi import Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Like
from app.token import verify_access_token
from app.db_models import Likes

router = APIRouter(
    tags=["Like"]
)      


@router.post("/like", status_code=status.HTTP_201_CREATED)
def like_post(like: Like, db: Session = Depends(get_db), current_user: int = Depends(verify_access_token)):
    existing_like = db.query(Likes).filter(Likes.post_id == like.post_id, Likes.user_id == current_user.id).first()
    
    if like.dir == 1:
        if existing_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already liked this post")
        
        new_like = Likes(post_id=like.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Post liked successfully"}
    else:
        if not existing_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")
        
        db.delete(existing_like)
        db.commit()
        return {"message": "Post unliked successfully"}