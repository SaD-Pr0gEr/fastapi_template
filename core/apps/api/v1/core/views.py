import logging
from typing import Annotated, Any

from fastapi import Request
from fastapi.params import Depends

from core.abstract import App
from core.dependencies.auth import auth_user
from core.services.example import ExampleService


logger = logging.getLogger(__name__)


async def core(request: Request) -> Any:
    logger.info("AUTH OR READONLY USER ENDPOINT")
    app: App = request.app
    await ExampleService(app).do_something()
    return {"status": app.config.app.APP_NAME}


async def auth_required(user: Annotated[str, Depends(auth_user)]) -> Any:
    print('PYLINT CRYING TO UNUSED USER', user)
    logger.info("AUTH USER ENDPOINT")
    return {"status": "COOL, AUTH LOGGING WORKED"}
