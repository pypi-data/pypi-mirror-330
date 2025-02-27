import grpc
from json import loads, JSONDecodeError
from typing import Generic, TypeVar, Type, Any

from loguru import logger
from pydantic import ValidationError

from .. import DefaultValue, ErrorDetails


T = TypeVar("T")


class _BaseGrpcErrorMeta(type):
    def __getitem__(cls, item: Any) -> type:
        """
        Handle the generic parameterization of the BaseGrpcError class.

        Args:
            item (Any): The type parameter for the error details.

        Returns:
            Type[BaseGrpcError]: A new class with the specified type parameter.
        """
        return type(f"{cls.__name__}[{item}]", (cls,), {"_type_params": item})


class BaseGrpcError(Exception, Generic[T], metaclass=_BaseGrpcErrorMeta):
    """Base exception class for handling gRPC errors."""

    __slots__ = ("_status_code", "_message", "_type")

    def __init__(
        self, status_code: grpc.StatusCode, message: str, default_value: DefaultValue[T] | None = None
    ) -> None:
        """
        Initialize the BaseGrpcError instance.

        Args:
            status_code (grpc.StatusCode): Status code representing the gRPC error type.
            message (str): Error message to be sent to the client.
            default_value (Union[DefaultValue[T], None], optional): Optional default value for the error.
        """
        self._status_code: grpc.StatusCode = status_code
        self._message = ErrorDetails[T](description=message, default_value=default_value)
        self._type: Type[T] = self._get_type_param()

    @property
    def message(self) -> ErrorDetails[T]:
        """
        Retrieve the error details.

        Returns:
            ErrorDetails[T]: The error details object containing description and optional default value.
        """
        return self._message

    @property
    def status_code(self) -> grpc.StatusCode:
        """
        Retrieve the gRPC status code associated with the error.

        Returns:
            grpc.StatusCode: The gRPC status code.
        """
        return self._status_code

    def abort(self, context: grpc.ServicerContext) -> None:
        """
        Abort the gRPC request with the provided error message.

        Args:
            context (grpc.ServicerContext): The gRPC server context to abort.
        """
        context.abort(self._status_code, self._message.model_dump_json(by_alias=True))

    def __str__(self) -> str:
        """
        Return a string representation of the error.

        Returns:
            str: A string representation of the error with its class name and message.
        """
        return f"<{self.__class__.__name__}: {self._message.description}>"

    @classmethod
    def extract_error(cls, exc: grpc.RpcError) -> ErrorDetails[T] | None:
        """
        Extract error details from a gRPC exception.

        Args:
            exc (grpc.RpcError): The gRPC exception to extract error details from.

        Returns:
            Union[ErrorDetails[T], None]: The extracted error details, or None if extraction fails.
        """
        details: str = getattr(exc, "details", lambda: "")()
        if not details:
            logger.warning("Details is empty")
            return None
        try:
            type_: Type[T] = cls._get_type_param()
            error = ErrorDetails[type_].model_validate(loads(details))  # type: ignore[valid-type]
            return error
        except JSONDecodeError:
            logger.warning("Details is not serializable")
        except ValidationError as ex:
            message = f"Cant read error with ErrorDetails: {ex.json()}"
            logger.warning(message)
        return None

    @classmethod
    def extract_default_value_from_error(cls, exc: grpc.RpcError) -> T | None:
        error: ErrorDetails[T] | None = cls.extract_error(exc)
        if error and error.default_value:
            return error.default_value.value
        logger.warning("Default value is not present!")
        return None

    @classmethod
    def _get_type_param(cls) -> Type[T]:
        """
        Retrieve the type parameter for the class.

        Returns:
            Type[T]: The type parameter.
        """
        if hasattr(cls, "_type_params"):
            type_: Type[T] = cls._type_params
            return type_
        raise TypeError(f"Type parameter not specified for {cls.__name__}")
