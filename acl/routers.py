
from sqlalchemy.orm import Session
from acl.schemas import UserProfileSchema
from core.base_routing import main_router as router
from fastapi import Depends, Request
from acl.service import get_user_profile
from database.connection import get_db


@router.get("/profile/{user_id}", response_model=UserProfileSchema)
def get_profile(request: Request, user_id: str, db: Session = Depends(get_db)):
    return get_user_profile(request, user_id, db)

