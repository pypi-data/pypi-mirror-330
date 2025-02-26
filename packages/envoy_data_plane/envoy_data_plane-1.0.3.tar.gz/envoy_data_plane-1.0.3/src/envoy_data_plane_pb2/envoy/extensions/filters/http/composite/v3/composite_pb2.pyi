from envoy.config.core.v3 import base_pb2 as _base_pb2
from envoy.config.core.v3 import config_source_pb2 as _config_source_pb2
from envoy.config.core.v3 import extension_pb2 as _extension_pb2
from udpa.annotations import migrate_pb2 as _migrate_pb2
from udpa.annotations import status_pb2 as _status_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Composite(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DynamicConfig(_message.Message):
    __slots__ = ("name", "config_discovery")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_DISCOVERY_FIELD_NUMBER: _ClassVar[int]
    name: str
    config_discovery: _config_source_pb2.ExtensionConfigSource
    def __init__(self, name: _Optional[str] = ..., config_discovery: _Optional[_Union[_config_source_pb2.ExtensionConfigSource, _Mapping]] = ...) -> None: ...

class ExecuteFilterAction(_message.Message):
    __slots__ = ("typed_config", "dynamic_config", "sample_percent")
    TYPED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    typed_config: _extension_pb2.TypedExtensionConfig
    dynamic_config: DynamicConfig
    sample_percent: _base_pb2.RuntimeFractionalPercent
    def __init__(self, typed_config: _Optional[_Union[_extension_pb2.TypedExtensionConfig, _Mapping]] = ..., dynamic_config: _Optional[_Union[DynamicConfig, _Mapping]] = ..., sample_percent: _Optional[_Union[_base_pb2.RuntimeFractionalPercent, _Mapping]] = ...) -> None: ...
