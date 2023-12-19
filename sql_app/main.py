from fastapi import  FastAPI
from sql_app.apis.base import router

def include_router(app:FastAPI):
    app.include_router( router)

def start_application():
    app = FastAPI( )
    include_router(app)
    return app

app = start_application()