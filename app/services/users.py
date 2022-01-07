from app.schemas.users import UserIn
from app.models.users import User
from app.db import database

from app.utils.security import get_password_hash

users = User.__table__


async def get_all_users():
    query = users.select()
    db_users = await database.fetch_all(query=query)

    return db_users


async def get_user_by_email(email: str):
    query = users.select().where(users.c.email == email)
    db_user = await database.fetch_one(query=query)

    return dict(db_user) if db_user else db_user


async def create_user(user: UserIn):
    data = user.dict()
    password = data.pop('password')
    hashed_password = get_password_hash(password)
    query = users.insert().values(**data, password=hashed_password, is_active=True)

    user_id = await database.execute(query=query)

    return {"id": user_id, **user.dict(), "is_active": True}
