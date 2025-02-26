from google.protobuf import wrappers_pb2 as _wrappers_pb2
from udpa.annotations import status_pb2 as _status_pb2
from udpa.annotations import versioning_pb2 as _versioning_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TlsInspector(_message.Message):
    __slots__ = ("enable_ja3_fingerprinting", "initial_read_buffer_size")
    ENABLE_JA3_FINGERPRINTING_FIELD_NUMBER: _ClassVar[int]
    INITIAL_READ_BUFFER_SIZE_FIELD_NUMBER: _ClassVar[int]
    enable_ja3_fingerprinting: _wrappers_pb2.BoolValue
    initial_read_buffer_size: _wrappers_pb2.UInt32Value
    def __init__(self, enable_ja3_fingerprinting: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., initial_read_buffer_size: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ...) -> None: ...
