from typing import Callable
from fastapi import FastAPI
from app.db import (
    engine,
    Base,
    database
)
from app.settings import get_settings


settings = get_settings()


async def connect_to_db(app: FastAPI) -> None:
    if settings.TESTING:
        Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)

    await database.connect()
    app.state._db = database


async def close_db_connection(app: FastAPI) -> None:
    if settings.TESTING:
        Base.metadata.drop_all(engine)

    await app.state._db.disconnect()


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app
