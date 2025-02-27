from typing import Callable, Iterator, TypeVar

import grpc
from grpc import (
    HandlerCallDetails,
    RpcMethodHandler,
    ServerInterceptor,
    unary_unary_rpc_method_handler,
    unary_stream_rpc_method_handler,
    stream_unary_rpc_method_handler,
    stream_stream_rpc_method_handler,
)

# Типы для запросов и ответов
ReqType = TypeVar("ReqType")
RespType = TypeVar("RespType")


class BaseInterceptor(ServerInterceptor):
    def intercept_service(
        self, continuation: Callable[[HandlerCallDetails], RpcMethodHandler], handler_call_details: HandlerCallDetails
    ) -> RpcMethodHandler:
        handler: RpcMethodHandler = continuation(handler_call_details)

        def new_handler(request: ReqType | Iterator[ReqType], context: grpc.ServicerContext) -> RpcMethodHandler:
            method_type: str = self._get_method_type(handler)
            if handler.unary_unary:
                return self.handle_method(handler.unary_unary, request, context, handler_call_details, method_type)
            elif handler.unary_stream:
                return self.handle_method(handler.unary_stream, request, context, handler_call_details, method_type)
            elif handler.stream_unary:
                return self.handle_method(handler.stream_unary, request, context, handler_call_details, method_type)
            else:  # FYI handler.stream_stream:
                return self.handle_method(handler.stream_stream, request, context, handler_call_details, method_type)

        # Создание соответствующего обработчика в зависимости от типа вызова
        return self._create_method_handler(handler, new_handler)

    @staticmethod
    def _create_method_handler(handler: RpcMethodHandler, new_handler: Callable) -> RpcMethodHandler:
        """Создает новый обработчик исходя из типа вызова."""
        if handler.unary_unary:
            return unary_unary_rpc_method_handler(
                new_handler,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        elif handler.unary_stream:
            return unary_stream_rpc_method_handler(
                new_handler,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        elif handler.stream_unary:
            return stream_unary_rpc_method_handler(
                new_handler,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        else:  # FYI: handler.stream_stream
            return stream_stream_rpc_method_handler(
                new_handler,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

    @staticmethod
    def _get_method_type(handler: RpcMethodHandler) -> str:
        """Определяет тип RPC метода по атрибутам обработчика."""
        if handler.unary_unary:
            return "unary-unary"
        elif handler.unary_stream:
            return "unary-stream"
        elif handler.stream_unary:
            return "stream-unary"
        else:  # FYI handler.stream_stream:
            return "stream-stream"

    def handle_method(
        self,
        method: Callable,
        request: ReqType | Iterator[ReqType],
        context: grpc.ServicerContext,
        handler_call_details: HandlerCallDetails,
        method_type: str,
    ) -> RespType | Iterator[RespType]:
        if "stream" in method_type.split("-")[1]:
            # Потоковый ответ (unary-stream или stream-stream)
            return self.handle_stream_response(method, request, context, handler_call_details, method_type)
        # Одиночный ответ (unary-unary или stream-unary)
        response: RespType = method(request, context)
        return response

    def handle_stream_response(
        self,
        method: Callable,
        request: ReqType | Iterator[ReqType],
        context: grpc.ServicerContext,
        handler_call_details: HandlerCallDetails,
        method_type: str,
    ) -> Iterator[RespType]:
        response_iterator = method(request, context)
        for response in response_iterator:
            yield response
