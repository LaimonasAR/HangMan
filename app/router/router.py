from fastapi import APIRouter

from endpoints import accounts_api, games_api

api_router = APIRouter()

api_router.include_router(accounts_api.router, prefix="/accounts", tags=["account"])
api_router.include_router(
    games_api.router,
    prefix="/games",
    tags=["games"],
)
