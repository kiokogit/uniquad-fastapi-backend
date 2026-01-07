import jwt
from typing import Any, Dict
from core.settings import settings


def decode_token(token: str) -> Dict[str, Any] | None:

    try:
        jwt_decoded = jwt.decode(token, key=str(settings.SECRET_KEY), algorithms=[settings.ALGORITHM], options={"verify_signature": True})
    except (jwt.PyJWTError, UnicodeDecodeError):
        return None
    return jwt_decoded
    



