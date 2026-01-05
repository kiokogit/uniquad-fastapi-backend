

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from posts.models import PostType

class CreatePostSchema(BaseModel):
    title: str | None # allow for comments
    description: str
    location: str | None
    time: datetime | None
    images: list[str, None]
    attendees: int | None
    author_id: UUID
    community_instance_id: UUID | None
    post_type: str
    price: int | None
    pin_location: str | None
    contact: str | None
    parent_post_id: UUID | None


class Profile(BaseModel):
    full_name: str
    avatar: str | None
    

class PostSchema(BaseModel):
    id: UUID
    title: str
    description: str
    location: str
    time: datetime
    images: list[str]
    attendees: int
    created_at: datetime
    updated_at: datetime
    author_id: UUID | str
    community_instance_id: UUID | None
    post_type: str
    likes: int | None
    price: int | None
    pin_location: str | None
    contact: str | None
    parent_post_id: UUID | None
    # created_by: Profile

    class Config:
        from_attributes = True
    
    
    # 
    # community_instance: CommunitySchema

class DetailedPostSchema(PostSchema):
    comments: list[PostSchema]

    class Config:
        from_attributes = True



