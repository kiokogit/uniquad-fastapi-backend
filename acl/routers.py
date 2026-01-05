
from acl.schemas import UserProfileSchema
from core.base_routing import main_router as router
from fastapi import Request
from acl.service import get_user_profile


@router.get("/profile", response_model=UserProfileSchema)
def get_profile(request: Request):
    return get_user_profile(request)