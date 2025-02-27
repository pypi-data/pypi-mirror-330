# agi-med-grpc-interceptors

Стандартные middlewares для grpc

## Ответственный разработчик

@zhelvakov

## Общая информация

- LoggingInterceptor - работает на loguru. Принимает metadata, забирает все хедеры и пытается использовать как контекст, по-умолчанию дополнительно прописывает uuid в контекст. Обработка ошибок может быть переопределена с помощью метода exception_handler
- ExcHandlerInterceptor - добавляет подсчет ошибок с помощью prometheus: error_counter[path, status_code, error]. Обрабатывает ошибки, которые наследуются от BaseGrpcError (Пример ниже) 


### Примеры

1. Подключение interceptors

```python
import grpc
from concurrent import futures

from agi_med_grpc_interceptors import LoggingInterceptor, ExcHandlerInterceptor


server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[LoggingInterceptor(), ExcHandlerInterceptor()],
    )
```

2. Реализация ошибки для сервиса

```python
#server
from agi_med_grpc_interceptors import BaseGrpcError, DefaultValue
from grpc import StatusCode

from .some_protos.Some_pb2_grpc import SomeServicer
from .Some_pb import GetSalaryResponse, GetSalaryRequest


class EmployerNotFound(BaseGrpcError[float]):
    def __init__(self, message: str) -> None:
        default_value = DefaultValue[float](value=0)
        super().__init__(StatusCode.ALREADY_EXISTS, message, default_value)

class Some(SomeServicer):
    def GetSalary(self, request: GetSalaryRequest) -> GetSalaryResponse:
        if request.Username == "bob":
            raise EmployerNotFound("Bob, go to home!")
        return GetSalaryResponse(salary=10_000)

#client
from agi_med_grpc_interceptors import BaseGrpcError, ErrorDetails
from grpc import RpcError

from .Some_pb import GetSalaryResponse, GetSalaryRequest
from .Some_pb2_grpc import SomeStub


stub = SomeStub("0.0.0.0:5000")

try:
    request = GetSalaryRequest(Username="bob")
    response: GetSalaryResponse = stub.DoSomething(request)
except RpcError as ex:
    error: ErrorDetails[float] | None = BaseGrpcError[float].extract_error(ex)
    default_value: float | None = BaseGrpcError[float].extract_default_value_from_error(ex)
    print(f"{error=}")
    print(f"{default_value=}")
```

### Линтеры

```shell
pip install black flake8-pyproject mypy
black .
flake8
mypy .
```
