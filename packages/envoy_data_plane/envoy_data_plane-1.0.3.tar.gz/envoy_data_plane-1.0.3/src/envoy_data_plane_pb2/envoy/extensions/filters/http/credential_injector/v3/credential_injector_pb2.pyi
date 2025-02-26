from envoy.config.core.v3 import extension_pb2 as _extension_pb2
from xds.annotations.v3 import status_pb2 as _status_pb2
from udpa.annotations import status_pb2 as _status_pb2_1
from validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CredentialInjector(_message.Message):
    __slots__ = ("overwrite", "allow_request_without_credential", "credential")
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    ALLOW_REQUEST_WITHOUT_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    overwrite: bool
    allow_request_without_credential: bool
    credential: _extension_pb2.TypedExtensionConfig
    def __init__(self, overwrite: bool = ..., allow_request_without_credential: bool = ..., credential: _Optional[_Union[_extension_pb2.TypedExtensionConfig, _Mapping]] = ...) -> None: ...
