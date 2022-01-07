from app.dependencies.authentication import (
    check_user,
    get_current_user,
    sign_jwt
)
from app.schemas.users import (
    Token,
    UserLogin,
    UserOut,
    UserIn
)
from app.services import users as db_manager_user

from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
    Body
)

from typing import List


users = APIRouter(prefix="/users", tags=["Users"])


@users.get('/', response_model=List[UserOut])
async def get_users():
    return await db_manager_user.get_all_users()


@users.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserIn):
    return await db_manager_user.create_user(payload)


@users.post("/token", response_model=Token)
async def login_for_access_token(user: UserLogin = Body(...)):
    if await check_user(user):
        return sign_jwt(user.email)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )


@users.get("/me", response_model=UserOut)
async def me(current_user: UserOut = Depends(get_current_user)):
    return current_user
