import jwt
from typing import Any, Dict
from core.settings import ALGORITHM, SECRET_KEY


def decode_token(token: str) -> Dict[str, Any] | None:

    try:
        jwt_decoded = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": True})
    except jwt.PyJWTError, UnicodeDecodeError:
        return None
    return jwt_decoded
    



