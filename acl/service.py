from sqlalchemy.orm import Session
from acl.models import UserProfile
from fastapi import Depends, Request

from database.connection import get_db



def get_user_profile(request: Request, user_id: str, db: Session = Depends(get_db)):
    if user_id == 'me':
        return request.state.user

    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()


