from pydantic import BaseModel


class ExampleDTO(BaseModel):
    status: int
