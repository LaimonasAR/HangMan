from fastapi import Depends, FastAPI, Request, Response
from router.router import api_router
from database.db import engine, Base
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

templates= Jinja2Templates(directory="templates")