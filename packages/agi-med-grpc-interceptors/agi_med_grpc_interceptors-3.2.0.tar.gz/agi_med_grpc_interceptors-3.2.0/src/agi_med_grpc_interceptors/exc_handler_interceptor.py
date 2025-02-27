from typing import Callable, Iterator, Never
from typing_extensions import override

from grpc import HandlerCallDetails, ServicerContext
from loguru import logger

from .base_interceptor import ReqType, RespType
from . import BaseInterceptor, BaseGrpcError


class ExcHandlerInterceptor(BaseInterceptor):

    @override
    def handle_method(  # type: ignore[override]
        self,
        method: Callable,
        request: ReqType | Iterator[ReqType],
        context: ServicerContext,
        handler_call_details: HandlerCallDetails,
        method_type: str,
    ) -> RespType | Iterator[RespType]:
        try:
            return super().handle_method(method, request, context, handler_call_details, method_type)
        except Exception as exc:
            self.exception_handler(exc, request, context, handler_call_details, method_type)

    @override
    def handle_stream_response(
        self,
        method: Callable,
        request: ReqType | Iterator[ReqType],
        context: ServicerContext,
        handler_call_details: HandlerCallDetails,
        method_type: str,
    ) -> Iterator[RespType]:
        try:
            yield from super().handle_stream_response(method, request, context, handler_call_details, method_type)
        except Exception as exc:
            self.exception_handler(exc, request, context, handler_call_details, method_type)

    def exception_handler(
        self,
        exc: Exception,
        request: ReqType | Iterator[ReqType],
        context: ServicerContext,
        handler_call_details: HandlerCallDetails,
        method_type: str,
    ) -> Never:
        method: str = handler_call_details.method
        if isinstance(exc, BaseGrpcError):
            logger.error(f"Error {exc} in {method_type} gRPC call: {method}. Pack to .abort()")
            logger.debug(f"Error request: {request}")
            exc.abort(context)  # сам grpc вызывает raise Exception()
        raise
