from dataclasses import dataclass


@dataclass
class APIErrorMessage:
    field_loc: list[str | int | bool]
    description: str


@dataclass
class ApiExceptionResponse:
    code: int
    detail: str | None = None
    messages: list[APIErrorMessage] | None = None
