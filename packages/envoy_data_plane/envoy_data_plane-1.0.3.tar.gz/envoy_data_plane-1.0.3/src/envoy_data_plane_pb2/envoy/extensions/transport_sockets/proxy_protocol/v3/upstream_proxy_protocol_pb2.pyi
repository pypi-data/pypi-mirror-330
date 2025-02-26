from envoy.config.core.v3 import base_pb2 as _base_pb2
from envoy.config.core.v3 import proxy_protocol_pb2 as _proxy_protocol_pb2
from udpa.annotations import status_pb2 as _status_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProxyProtocolUpstreamTransport(_message.Message):
    __slots__ = ("config", "transport_socket")
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_SOCKET_FIELD_NUMBER: _ClassVar[int]
    config: _proxy_protocol_pb2.ProxyProtocolConfig
    transport_socket: _base_pb2.TransportSocket
    def __init__(self, config: _Optional[_Union[_proxy_protocol_pb2.ProxyProtocolConfig, _Mapping]] = ..., transport_socket: _Optional[_Union[_base_pb2.TransportSocket, _Mapping]] = ...) -> None: ...
