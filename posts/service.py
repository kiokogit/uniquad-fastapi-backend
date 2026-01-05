from uuid import UUID
from fastapi import Request, Depends, HTTPException
from fastapi_pagination import paginate
from sqlalchemy.orm import Session, joinedload
from posts.schema import CreatePostSchema
from posts.models import Post, PostType
from database.connection import get_db


def create_post(request: Request, post: CreatePostSchema, db: Session = Depends(get_db)):

    post = Post(**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message": "Post created successfully"}


def fetch_posts(request: Request, post_type: PostType, db: Session = Depends(get_db)):
    posts = (
        db.query(Post)
        # .options(
        #     joinedload(Post.created_by), 
        #     # joinedload(Post.community_instance)
        #     )
        .filter(Post.post_type == post_type.value)).all()
    return paginate(posts)


def fetch_post(request: Request, post_id: UUID, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).one_or_none()
    # .options(
    #         joinedload(Post.created_by),
    #         joinedload(Post.community_instance),
        # )
    if not post:
        raise HTTPException(status_code=400, detail="Invalid post ID")
    comments = db.query(Post).filter(Post.parent_post_id == post.id, Post.post_type == 'comment').all()
    post.comments = comments
    return post



