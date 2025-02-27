from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")


class DefaultValue(BaseModel, Generic[T]):
    value: T
