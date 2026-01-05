from database.connection import Base
from sqlalchemy import Column, String, UUID
import uuid


class CommunityInstance(Base):
    __tablename__ = "community_instances"

    id = Column[UUID[str]](UUID, primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    name = Column[str](String, unique=True, index=True, nullable=False)
    initials = Column[str](String, unique=True, index=True, nullable=False)
    description = Column[str](String, nullable=True)
    location = Column[str](String, nullable=True)


class UserProfile(Base):
    # store basic user information as one in fusionAuth for ease of serialization of information

    __tablename__ = "user_profiles"

    id = Column[UUID[str]](UUID, primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    user_id = Column[str](String, unique=True, index=True, nullable=False) 
    full_name = Column[str](String, nullable=False)
    email = Column[str](String, unique=True, index=True, nullable=False)
    community_instance_id = Column[UUID[str]](UUID, nullable=False)  # ForeignKey can be added later
    role = Column[str](String, nullable=False)  # e.g., 'student', 'external', 'admin'
    avatar_url = Column[str](String, nullable=True)
    

