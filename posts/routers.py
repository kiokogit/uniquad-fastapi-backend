from uuid import UUID
from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.orm import Session
from core.dependencies import TokenBearer
from database.connection import get_db
from posts.models import PostType
from posts.service import create_post, fetch_posts, fetch_post
from posts.schema import CreatePostSchema, DetailedPostSchema, PostSchema
from core.base_routing import main_router as router
from fastapi_pagination import Page


@router.post("/posts/create", response_model=dict)
def create_post_route(request: Request, post: CreatePostSchema, db: Session = Depends(get_db)):
    return create_post(request, post, db)

@router.get("/posts/fetch", response_model=Page[PostSchema])
def fetch_posts_route(request: Request, post_type: PostType = Query(..., description="The type of post to fetch"), db: Session = Depends(get_db)):
    return fetch_posts(request, post_type, db)

@router.get("/posts/fetch/{post_id}", response_model=DetailedPostSchema)
def fetch_post_route(request: Request, post_id: UUID, db: Session = Depends(get_db)):
    return fetch_post(request, post_id, db)

