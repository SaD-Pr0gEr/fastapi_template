from typing import Any

from fastapi import Request

from core.abstract import App
from core.services.example import ExampleService


async def core(request: Request) -> Any:
    app: App = request.app
    await ExampleService(app).do_something()
    return {"status": app.config.app.APP_NAME}
