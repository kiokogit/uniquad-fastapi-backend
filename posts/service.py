from typing import Any


from uuid import UUID
from fastapi import BackgroundTasks, Request, Depends, HTTPException, Query, background
from fastapi_pagination import paginate
from sqlalchemy.orm import Session, joinedload
from background_tasks.celery_app import index_documents
from posts.schema import CreatePostSchema, PostSchema
from posts.models import Post, PostType
from database.connection import get_db
from sqlalchemy import desc, asc


async def create_post(request: Request, post: CreatePostSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    post.author_id = request.state.user.user_id
    post.community_instance_id = request.state.user.community_instance_id
    post = Post(**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)

    indexing_data = {
        'title': post.title,
        'description': post.description,
        'id': str(post.id),
        'author_id': str(post.author_id),
        'created_at': post.created_at,
        'location': post.location
    }

    # background_tasks.add_task(index_documents, 'events', [indexing_data])
    # celery_app.send_task('index_documents', args=['events', [indexing_data]])
    index_documents.delay('events', [indexing_data])
    # index_documents.apply_async(args=['events', [indexing_data]])


    return {"message": "Post created successfully"}

ORDER_MAP = {
    "newest": desc(Post.created_at),
    "oldest": asc(Post.created_at),
    "most_liked": desc(Post.likes),
    "most_attended": desc(Post.attendees),
}

def fetch_posts(request: Request, post_type: PostType, order_by: str = Query("newest"), db: Session = Depends(get_db)):
    posts = (
        db.query(Post)
        .options(
            joinedload(Post.created_by),
            joinedload(Post.community_instance),
        )
        .filter(Post.post_type == post_type.value).order_by(ORDER_MAP.get(order_by, desc(Post.created_at)))).all()
    return paginate(posts)


def fetch_post(request: Request, post_id: UUID, db: Session = Depends(get_db)):
    post = (
        db.query(Post).filter(Post.id == post_id)
        .options(
            joinedload(Post.created_by),
            joinedload(Post.community_instance),
        )
        ).one_or_none()
    
    if not post:
        raise HTTPException(status_code=400, detail="Invalid post ID")
    comments = db.query(Post).filter(Post.parent_post_id == post.id, Post.post_type == 'comment').all()
    post.comments = comments
    return post

def act_on_post_post(post_id: UUID, action_type: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).one_or_none()
    if not post:
        raise HTTPException(status_code=400, detail="Post not found")
    if action_type == 'like':
        if post.likes in [None, 0]:
            post.likes = 1
        else:
            post.likes = post.likes + 1
    if action_type == 'attend':
        post.attendees = 1 if post.attendees in [None, 0] else post.attendees + 1
        
    db.commit()
    return {"message": "Updated successfully"}
    
 


