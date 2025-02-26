from envoy.config.core.v3 import base_pb2 as _base_pb2
from google.protobuf import any_pb2 as _any_pb2
from udpa.annotations import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CapabilityRestrictionConfig(_message.Message):
    __slots__ = ("allowed_capabilities",)
    class AllowedCapabilitiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: SanitizationConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[SanitizationConfig, _Mapping]] = ...) -> None: ...
    ALLOWED_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    allowed_capabilities: _containers.MessageMap[str, SanitizationConfig]
    def __init__(self, allowed_capabilities: _Optional[_Mapping[str, SanitizationConfig]] = ...) -> None: ...

class SanitizationConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class VmConfig(_message.Message):
    __slots__ = ("vm_id", "runtime", "code", "configuration", "allow_precompiled", "nack_on_code_cache_miss", "environment_variables")
    VM_ID_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    ALLOW_PRECOMPILED_FIELD_NUMBER: _ClassVar[int]
    NACK_ON_CODE_CACHE_MISS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    vm_id: str
    runtime: str
    code: _base_pb2.AsyncDataSource
    configuration: _any_pb2.Any
    allow_precompiled: bool
    nack_on_code_cache_miss: bool
    environment_variables: EnvironmentVariables
    def __init__(self, vm_id: _Optional[str] = ..., runtime: _Optional[str] = ..., code: _Optional[_Union[_base_pb2.AsyncDataSource, _Mapping]] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., allow_precompiled: bool = ..., nack_on_code_cache_miss: bool = ..., environment_variables: _Optional[_Union[EnvironmentVariables, _Mapping]] = ...) -> None: ...

class EnvironmentVariables(_message.Message):
    __slots__ = ("host_env_keys", "key_values")
    class KeyValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    HOST_ENV_KEYS_FIELD_NUMBER: _ClassVar[int]
    KEY_VALUES_FIELD_NUMBER: _ClassVar[int]
    host_env_keys: _containers.RepeatedScalarFieldContainer[str]
    key_values: _containers.ScalarMap[str, str]
    def __init__(self, host_env_keys: _Optional[_Iterable[str]] = ..., key_values: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PluginConfig(_message.Message):
    __slots__ = ("name", "root_id", "vm_config", "configuration", "fail_open", "capability_restriction_config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOT_ID_FIELD_NUMBER: _ClassVar[int]
    VM_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    FAIL_OPEN_FIELD_NUMBER: _ClassVar[int]
    CAPABILITY_RESTRICTION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    root_id: str
    vm_config: VmConfig
    configuration: _any_pb2.Any
    fail_open: bool
    capability_restriction_config: CapabilityRestrictionConfig
    def __init__(self, name: _Optional[str] = ..., root_id: _Optional[str] = ..., vm_config: _Optional[_Union[VmConfig, _Mapping]] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., fail_open: bool = ..., capability_restriction_config: _Optional[_Union[CapabilityRestrictionConfig, _Mapping]] = ...) -> None: ...

class WasmService(_message.Message):
    __slots__ = ("config", "singleton")
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    SINGLETON_FIELD_NUMBER: _ClassVar[int]
    config: PluginConfig
    singleton: bool
    def __init__(self, config: _Optional[_Union[PluginConfig, _Mapping]] = ..., singleton: bool = ...) -> None: ...
