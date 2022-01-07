from fastapi import FastAPI

from app.db import (
    engine,
    Base,
    database
)
from app.routers.users import users


Base.metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", tags=["Index"])
async def index():
    return {"message": "Hello World"}


app.include_router(users)
