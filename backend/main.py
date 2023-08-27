from fastapi import FastAPI
from router.router import api_router
from database.db import engine, Base
from fastapi.templating import Jinja2Templates

Base.metadata.create_all(bind=engine)
api = FastAPI()
api.include_router(api_router, prefix="/api/v1")

templates = Jinja2Templates(directory="templates")
