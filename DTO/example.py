from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class ExampleDTO(BaseModel):
    status: str
