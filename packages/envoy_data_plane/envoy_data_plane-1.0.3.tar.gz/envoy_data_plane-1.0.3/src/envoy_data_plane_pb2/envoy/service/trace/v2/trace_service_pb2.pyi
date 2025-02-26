from envoy.api.v2.core import base_pb2 as _base_pb2
from envoy.api.v2.core import socket_option_pb2 as _socket_option_pb2
from opencensus.proto.trace.v1 import trace_pb2 as _trace_pb2
from udpa.annotations import status_pb2 as _status_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StreamTracesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StreamTracesMessage(_message.Message):
    __slots__ = ("identifier", "spans")
    class Identifier(_message.Message):
        __slots__ = ("node",)
        NODE_FIELD_NUMBER: _ClassVar[int]
        node: _base_pb2.Node
        def __init__(self, node: _Optional[_Union[_base_pb2.Node, _Mapping]] = ...) -> None: ...
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    SPANS_FIELD_NUMBER: _ClassVar[int]
    identifier: StreamTracesMessage.Identifier
    spans: _containers.RepeatedCompositeFieldContainer[_trace_pb2.Span]
    def __init__(self, identifier: _Optional[_Union[StreamTracesMessage.Identifier, _Mapping]] = ..., spans: _Optional[_Iterable[_Union[_trace_pb2.Span, _Mapping]]] = ...) -> None: ...
