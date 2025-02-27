from pydantic import BaseModel, Field, ConfigDict
from typing import Generic, TypeVar

from . import DefaultValue

T = TypeVar("T")


class ErrorDetails(BaseModel, Generic[T]):
    model_config = ConfigDict(populate_by_name=True)

    description: str
    default_value: DefaultValue[T] | None = Field(None, alias="defaultValue")
