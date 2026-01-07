

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator

class CreatePostSchema(BaseModel):
    title: str | None # allow for comments
    description: str
    location: str | None = Field(default=None)
    time: Optional[datetime] = None
    images: list[str] = Field(default=[])
    author_id: UUID | None = Field(default=None)
    community_instance_id: UUID | None = Field(default=None)
    post_type: str
    price: int = Field(default=120)
    pin_location: str | None
    contact: str | None = Field(default=None)
    parent_post_id: UUID | None = Field(default=None)

    @model_validator(mode='after') # this mode is for parsed data
    def validate_contact(self):
        if self.post_type == 'ad' and not self.contact:
            raise ValueError('Contact is required for an ad')
        return self



class Profile(BaseModel):
    full_name: str
    avatar_url: Optional[str]
    user_id: str
    

class PostSchema(BaseModel):
    id: UUID
    title: str | None
    description: str
    location: str | None
    time: datetime | None
    images: list[str]
    attendees: int | None
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
    created_by: Profile

    model_config = ConfigDict(extra='ignore')
    

class DetailedPostSchema(PostSchema):
    comments: list[PostSchema]




