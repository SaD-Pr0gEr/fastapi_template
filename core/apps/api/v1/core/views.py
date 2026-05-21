import logging
from typing import Annotated, Any

from fastapi import Request
from fastapi.params import Depends

from DTO.example import ExampleDTO
from DTO.exceptions import APIErrorMessage
from core.abstract import App
from core.dependencies.auth import auth_user
from core.services.example import ExampleService
from utils.exceptions import BadRequestHTTPException

logger = logging.getLogger(__name__)


async def core(request: Request) -> Any:
    logger.info("AUTH OR READONLY USER ENDPOINT")
    app: App = request.app
    await ExampleService(app).do_something()
    return {"status": 200}


async def auth_required(user: Annotated[str, Depends(auth_user)]) -> Any:
    print("PYLINT CRYING TO UNUSED USER", user)
    logger.info("AUTH USER ENDPOINT")
    return {"status": 200}


async def exp_exception(body: ExampleDTO):
    print(body, 'is valid')
    raise BadRequestHTTPException(
        400,
        "Without pydantic validation",
        [APIErrorMessage(["cart_items", 0, "name"], "this field is trash")],
    )
