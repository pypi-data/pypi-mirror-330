from envoy.config.core.v3 import base_pb2 as _base_pb2
from envoy.annotations import deprecation_pb2 as _deprecation_pb2
from udpa.annotations import status_pb2 as _status_pb2
from udpa.annotations import versioning_pb2 as _versioning_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Lua(_message.Message):
    __slots__ = ("inline_code", "source_codes", "default_source_code", "stat_prefix")
    class SourceCodesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _base_pb2.DataSource
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_base_pb2.DataSource, _Mapping]] = ...) -> None: ...
    INLINE_CODE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CODES_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_SOURCE_CODE_FIELD_NUMBER: _ClassVar[int]
    STAT_PREFIX_FIELD_NUMBER: _ClassVar[int]
    inline_code: str
    source_codes: _containers.MessageMap[str, _base_pb2.DataSource]
    default_source_code: _base_pb2.DataSource
    stat_prefix: str
    def __init__(self, inline_code: _Optional[str] = ..., source_codes: _Optional[_Mapping[str, _base_pb2.DataSource]] = ..., default_source_code: _Optional[_Union[_base_pb2.DataSource, _Mapping]] = ..., stat_prefix: _Optional[str] = ...) -> None: ...

class LuaPerRoute(_message.Message):
    __slots__ = ("disabled", "name", "source_code")
    DISABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CODE_FIELD_NUMBER: _ClassVar[int]
    disabled: bool
    name: str
    source_code: _base_pb2.DataSource
    def __init__(self, disabled: bool = ..., name: _Optional[str] = ..., source_code: _Optional[_Union[_base_pb2.DataSource, _Mapping]] = ...) -> None: ...
