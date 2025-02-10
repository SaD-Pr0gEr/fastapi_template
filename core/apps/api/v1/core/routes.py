from fastapi import APIRouter

from DTO.example import ExampleDTO
from core.abstract import App
from . import views


def register_core_routes(app: App) -> APIRouter:
    api_router = APIRouter(prefix="/core")
    api_router.add_api_route(
        "/", endpoint=views.core, name=app.config.urls.CORE_GET,
        response_model=ExampleDTO
    )
    return api_router
