from uuid import UUID
from pydantic import BaseModel


class CommunityInstanceSchema(BaseModel):
    id: str
    name: str
    initials: str
    description: str | None = None
    location: str | None = None


class UserProfileSchema(BaseModel):
    id: UUID
    user_id: str
    full_name: str
    email: str
    community_instance_id: UUID
    role: str
    avatar_url: str | None = None


