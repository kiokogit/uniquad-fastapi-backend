from uuid import UUID

from sqlalchemy.orm import Session
from database.connection import get_db
from fastapi.security import HTTPBearer
from acl.utils import decode_token
from fastapi import Depends, HTTPException, Request
from acl.models import UserProfile as UserModel


class TokenBearer(HTTPBearer):
    """
    A custom FastAPI HTTPBearer dependency that validates and decodes JWT
    access tokens, retrieves or creates a user profile from the database,
    and attaches the user profile to `request.state.user`.

    On successful authentication, the user object is returned and can be used as a dependency.
    If authentication or user retrieval fails, a 401 HTTPException is raised.
    """
    def __init__(self):
        super().__init__(auto_error=True)

    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        creds = await super().__call__(request)
        if creds is None:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")
        token = creds.credentials
        token_data = decode_token(token)

        if not token_data:
            raise HTTPException(status_code=401, detail="Invalid permissions")
        try:
            user_id = UUID(token_data["sub"])
        except Exception:
            raise HTTPException(401, 'Well, cant see why is this')
        user = db.query(UserModel).filter(UserModel.user_id == str(user_id)).one_or_none()
        if not user:
            # create new user profile
            user = UserModel(
                user_id=str(user_id),
                full_name=token_data.get("user_metadata", {}).get("full_name", "Unnamed User"),
                avatar_url=token_data.get("user_metadata", {}).get("avatar_url", None),
                email=token_data.get("email"),
                role="student",
                community_instance_id=UUID("00000000-0000-0000-0000-000000000000")  # default instance
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        request.state.user = user
        return user
        
token_bearer = TokenBearer()

