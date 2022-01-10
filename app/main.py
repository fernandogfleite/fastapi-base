from fastapi import FastAPI
from app.routers.users import users
from app.core import tasks


def create_application():
    app = FastAPI()

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(users)

    return app


app = create_application()


@app.get("/", tags=["Index"])
async def index():
    return {"message": "Hello World"}
