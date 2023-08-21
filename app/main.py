from fastapi import Depends, FastAPI, Request, Response, Form, HTTPException
from router.router import api_router
from database.db import engine, Base
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from endpoints import accounts_api
import httpx
from jose import JWTError, jwt
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

templates = Jinja2Templates(directory="templates")


# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/v1/accounts/")

    if response.status_code == 200:
        data = response.json()  # Assuming the response contains JSON data
        # return data
    else:
        return {"error": "Failed to fetch data from API"}
    user_one = data[0]
    user_one_name = user_one["name"]
    context = {"request": request, "users": user_one_name}
    # users= accounts_api.read_accounts()
    return templates.TemplateResponse("index.html", context)


@app.post("/submit", response_class=HTMLResponse)
async def index(
    request: Request,
    name: str = Form(...),
    surname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    data = {"name": name, "surname": surname, "email": email, "password": password}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/accounts/", json=data
        )

    if response.status_code == 200:
        # return {"message": "Data posted successfully"}
        context = {"request": request, "message": "Data posted successfully"}
        # return templates.TemplateResponse("login.html", context)
        return RedirectResponse(url="/login")
    else:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to post data to API"
        )


@app.get("/login", response_class=HTMLResponse)
async def index(request: Request):
    # async with httpx.AsyncClient() as client:
    #     response = await client.get("http://localhost:8000/api/v1/accounts/")

    # if response.status_code == 200:
    #     data = response.json()  # Assuming the response contains JSON data
    #     # return data
    # else:
    #     return {"error": "Failed to fetch data from API"}
    # user_one = data[0]
    # user_one_name = user_one["name"]
    # context = {"request": request, "users": user_one_name}
    context = {"request": request}
    # users= accounts_api.read_accounts()
    return templates.TemplateResponse("login.html", context)

