from typing import Any, TypeAlias

from connectrpc.interceptor import (
    BidiStreamInterceptor,
    ClientStreamInterceptor,
    MetadataInterceptor,
    ServerStreamInterceptor,
    UnaryInterceptor,
)

Interceptors: TypeAlias = tuple[
    UnaryInterceptor
    | ClientStreamInterceptor
    | ServerStreamInterceptor
    | BidiStreamInterceptor
    | MetadataInterceptor[Any],
    ...,
]
