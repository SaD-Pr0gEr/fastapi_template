from dataclasses import asdict
from typing import Any

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from DTO.exceptions import APIErrorMessage, ApiExceptionResponse


class AbstractJsonException(HTTPException):
    _status_code: int
    _detail: str | None = None
    _errors: list[APIErrorMessage] | None = None

    def __init__(
        self,
        status_: int,
        detail_: str | None = None,
        errors: list[APIErrorMessage] | None = None,
    ) -> None:
        status_ = status_ if status_ else self._status_code
        detail_ = detail_ if detail_ else self._detail
        super().__init__(status_code=status_, detail=detail_)
        self._errors = errors or []

    def response(self) -> dict[int | str, str | Any] | None:
        return asdict(
            ApiExceptionResponse(self._status_code, self._detail, self._errors)
        )


class UnauthorizedHTTPException(AbstractJsonException):
    _status_code = status.HTTP_401_UNAUTHORIZED
    _detail = "Вы не авторизованы"


class ForbiddenHTTPException(AbstractJsonException):
    _status_code = status.HTTP_403_FORBIDDEN
    _detail = "У вас недостаточно прав на этот ресурс"


class NotFoundHTTPException(AbstractJsonException):
    _status_code = status.HTTP_404_NOT_FOUND
    _detail = "Объект не найден"


class NotAcceptableHTTPException(AbstractJsonException):
    _status_code = status.HTTP_406_NOT_ACCEPTABLE
    _detail = "Запрос не принимается"


class BadRequestHTTPException(AbstractJsonException):
    _status_code = status.HTTP_400_BAD_REQUEST
    _detail = "Некорректный запрос"


class ServerErrorHTTPException(AbstractJsonException):
    _status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    _detail = "Ошибка сервера"


async def custom_json_exception_handler(
    request: Request, exc: AbstractJsonException
) -> JSONResponse:
    return JSONResponse(exc.response(), status_code=exc.status_code)


async def rewrite_builtin_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    errors = []
    for err in exc.errors():
        errors.append(APIErrorMessage(err["loc"][1:], err["msg"]))
    return JSONResponse(
        asdict(ApiExceptionResponse(400, "Невалидные данные", errors))
    )
