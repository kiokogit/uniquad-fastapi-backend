from acl.schemas import UserProfileSchema
from fastapi import Request



def get_user_profile(request: Request):

    return request.state.user


