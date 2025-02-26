from envoy.extensions.transport_sockets.tls.v3 import secret_pb2 as _secret_pb2
from xds.annotations.v3 import status_pb2 as _status_pb2
from udpa.annotations import status_pb2 as _status_pb2_1
from validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Generic(_message.Message):
    __slots__ = ("credential", "header")
    CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    credential: _secret_pb2.SdsSecretConfig
    header: str
    def __init__(self, credential: _Optional[_Union[_secret_pb2.SdsSecretConfig, _Mapping]] = ..., header: _Optional[str] = ...) -> None: ...
