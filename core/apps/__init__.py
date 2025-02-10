from core.abstract import App
from core.apps.api import register_api_routes


def register_app_routes(app: App):
    app.include_router(register_api_routes(app))
