from fastapi import Depends, FastAPI, Request, Response, Form, HTTPException
from router.router import api_router
from database.db import engine, Base
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from endpoints import accounts_api
import httpx

Base.metadata.create_all(bind=engine)
api = FastAPI()
api.include_router(api_router, prefix="/api/v1")

templates = Jinja2Templates(directory="templates")


# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})

