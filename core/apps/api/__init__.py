from fastapi import APIRouter

from core.abstract import App
from core.apps.api.v1 import register_v1_api_routes


def register_api_routes(app: App) -> APIRouter:
    api_router = APIRouter(prefix="/api")
    api_router.include_router(register_v1_api_routes(app))
    return api_router
