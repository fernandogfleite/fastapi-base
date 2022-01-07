from app.schemas.users import UserLogin
from app.utils.security import verify_password
from app.settings import get_settings
from app.services import users as db_manager_user

from fastapi import (
    HTTPException,
    Request,
    Depends
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from datetime import (
    datetime,
    timedelta
)
from typing import Dict

import time
import jwt


settings = get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def token_response(token: str):
    return {
        "access_token": token
    }


def sign_jwt(email: str) -> Dict[str, str]:
    payload = {
        "email": email,
        "expires": (datetime.now() + timedelta(minutes=30)).timestamp()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None

    except Exception:
        return {}


async def check_user(data: UserLogin):
    user = await db_manager_user.get_user_by_email(data.email)
    if user:
        if verify_password(data.password, user['password']):
            return True

    return False


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")

            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")

            return credentials.credentials

        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)

        except Exception:
            payload = None

        if payload:
            isTokenValid = True

        return isTokenValid


async def get_current_user(token: str = Depends(JWTBearer())):
    decoded_token = decode_jwt(token)

    email = decoded_token.get('email')

    return await db_manager_user.get_user_by_email(email)
