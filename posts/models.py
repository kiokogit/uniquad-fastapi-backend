from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Index
from database.connection import Base
from sqlalchemy import Column, String, UUID, DateTime, Integer, ARRAY
import uuid
from datetime import timezone, datetime
from typing import Optional



class PostType(Enum):
    EVENT = "event"
    COMMENT = "comment"
    AD = "ad"
    REVIEW = "review"


class Post(Base):
    __tablename__ = "posts"

    id = Column[UUID[str]](UUID, primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    title = Column[Optional[str]](String, nullable=True)
    description = Column[Optional[str]](String, nullable=False)
    location = Column[Optional[str]](String, nullable=True)
    time = Column[Optional[datetime]](DateTime, nullable=True)
    images = Column[Optional[list[str]]](ARRAY(String), nullable=True)
    attendees = Column[Optional[int]](Integer, nullable=True)
    created_at = Column[datetime](DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column[datetime](DateTime, nullable=False, default=datetime.now(timezone.utc))
    author_id = Column[str](String, nullable=False)
    community_instance_id = Column[UUID[str]](UUID, nullable=True)
    post_type = Column[str](String, nullable=False)
    likes = Column[Optional[int]](Integer, nullable=True, default=0)
    price = Column[Optional[int]](Integer, nullable=True)
    pin_location = Column[Optional[str]](String, nullable=True)
    contact = Column[Optional[str]](String, nullable=True)
    parent_post_id = Column[Optional[UUID[str]]](UUID, nullable=True)

     # 🔗 Relationships
    created_by = relationship(
        "UserProfile",
        primaryjoin="foreign(Post.author_id) == UserProfile.user_id",
        lazy="joined",
        viewonly=True,
    )

    community_instance = relationship(
        "CommunityInstance",
        primaryjoin="foreign(Post.community_instance_id) == CommunityInstance.id",
        lazy="joined",
        viewonly=True,
    )


    __table_args__ = (
        Index("idx_posts_author_id", "author_id"),
        Index("idx_posts_community_instance_id", "community_instance_id"),
        Index("idx_posts_post_type", "post_type"),
    )
