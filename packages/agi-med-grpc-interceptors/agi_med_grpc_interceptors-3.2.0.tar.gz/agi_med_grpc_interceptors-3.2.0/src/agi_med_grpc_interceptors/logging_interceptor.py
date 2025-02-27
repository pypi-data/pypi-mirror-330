from typing import Callable, Iterator, Never
from typing_extensions import override


from grpc import HandlerCallDetails, RpcMethodHandler, ServicerContext
from loguru import logger

from . import BaseInterceptor
from .base_interceptor import ReqType, RespType


class LoggingInterceptor(BaseInterceptor):

    @override
    def intercept_service(
        self, continuation: Callable[[HandlerCallDetails], RpcMethodHandler], handler_call_details: HandlerCallDetails
    ) -> RpcMethodHandler:
        handler: RpcMethodHandler = continuation(handler_call_details)

        def new_handler(request: ReqType | Iterator[ReqType], context: ServicerContext) -> RpcMethodHandler:
            with logger.contextualize(request_id=request.RequestId):
                method_type: str = self._get_method_type(handler)
                if handler.unary_unary:
                    return self.handle_method(handler.unary_unary, request, context, handler_call_details, method_type)
                elif handler.unary_stream:
                    return self.handle_method(handler.unary_stream, request, context, handler_call_details, method_type)
                elif handler.stream_unary:
                    return self.handle_method(handler.stream_unary, request, context, handler_call_details, method_type)
                else:  # FYI handler.stream_stream:
                    return self.handle_method(
                        handler.stream_stream, request, context, handler_call_details, method_type
                    )

        # Создание соответствующего обработчика в зависимости от типа вызова
        return self._create_method_handler(handler, new_handler)

    @override
    def handle_method(  # type: ignore[override]
        self,
        method: Callable,
        request: ReqType | Iterator[ReqType],
        context: ServicerContext,
        handler_call_details: HandlerCallDetails,
        method_type: str,
    ) -> RespType | Iterator[RespType]:
        """Обрабатывает любой тип gRPC метода (unary или stream) с логированием."""
        try:
            return super().handle_method(method, request, context, handler_call_details, method_type)
        except Exception as e:
            self._log_method_error(method_type, handler_call_details, e, request)

    @override
    def handle_stream_response(
        self,
        method: Callable,
        request: ReqType | Iterator[ReqType],
        context: ServicerContext,
        handler_call_details: HandlerCallDetails,
        method_type: str,
    ) -> Iterator[RespType]:
        """Генерирует потоковый ответ с логированием."""
        try:
            response_iterator = method(request, context)
            for response in response_iterator:
                yield response
            self._log_method_completion(method_type, handler_call_details)
        except Exception as e:
            yield self._log_method_error(method_type, handler_call_details, e, request)

    @staticmethod
    def _log_method_call(
        method_type: str,
        handler_call_details: HandlerCallDetails,
    ) -> None:
        """Логирует начало вызова метода."""
        logger.info(f"Handling {method_type} gRPC call: {handler_call_details.method}")

    @staticmethod
    def _log_method_completion(
        method_type: str,
        handler_call_details: HandlerCallDetails,
    ) -> None:
        """Логирует завершение вызова метода."""
        logger.info(f"Completed {method_type} gRPC call: {handler_call_details.method}")

    @staticmethod
    def _log_method_error(
        method_type: str, handler_call_details: HandlerCallDetails, ex: Exception, request: ReqType | Iterator[ReqType]
    ) -> Never:
        """Логирует ошибку, возникшую во время вызова метода."""
        if type(ex) is Exception:  # isinstance ex Exception будет всегда True
            logger.debug("Skip full exception logging. Guess it is a .abort()")
        else:
            logger.error(f"Exception in {method_type} gRPC call: {handler_call_details.method}, request: {request}")
            logger.exception(ex)
        raise ex
