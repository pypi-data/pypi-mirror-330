from envoy.config.core.v3 import base_pb2 as _base_pb2
from envoy.config.core.v3 import extension_pb2 as _extension_pb2
from envoy.config.ratelimit.v3 import rls_pb2 as _rls_pb2
from envoy.config.route.v3 import route_components_pb2 as _route_components_pb2
from envoy.type.metadata.v3 import metadata_pb2 as _metadata_pb2
from envoy.type.v3 import http_status_pb2 as _http_status_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from udpa.annotations import status_pb2 as _status_pb2
from udpa.annotations import versioning_pb2 as _versioning_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RateLimit(_message.Message):
    __slots__ = ("domain", "stage", "request_type", "timeout", "failure_mode_deny", "rate_limited_as_resource_exhausted", "rate_limit_service", "enable_x_ratelimit_headers", "disable_x_envoy_ratelimited_header", "rate_limited_status", "response_headers_to_add", "status_on_error", "stat_prefix")
    class XRateLimitHeadersRFCVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OFF: _ClassVar[RateLimit.XRateLimitHeadersRFCVersion]
        DRAFT_VERSION_03: _ClassVar[RateLimit.XRateLimitHeadersRFCVersion]
    OFF: RateLimit.XRateLimitHeadersRFCVersion
    DRAFT_VERSION_03: RateLimit.XRateLimitHeadersRFCVersion
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    FAILURE_MODE_DENY_FIELD_NUMBER: _ClassVar[int]
    RATE_LIMITED_AS_RESOURCE_EXHAUSTED_FIELD_NUMBER: _ClassVar[int]
    RATE_LIMIT_SERVICE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_X_RATELIMIT_HEADERS_FIELD_NUMBER: _ClassVar[int]
    DISABLE_X_ENVOY_RATELIMITED_HEADER_FIELD_NUMBER: _ClassVar[int]
    RATE_LIMITED_STATUS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_HEADERS_TO_ADD_FIELD_NUMBER: _ClassVar[int]
    STATUS_ON_ERROR_FIELD_NUMBER: _ClassVar[int]
    STAT_PREFIX_FIELD_NUMBER: _ClassVar[int]
    domain: str
    stage: int
    request_type: str
    timeout: _duration_pb2.Duration
    failure_mode_deny: bool
    rate_limited_as_resource_exhausted: bool
    rate_limit_service: _rls_pb2.RateLimitServiceConfig
    enable_x_ratelimit_headers: RateLimit.XRateLimitHeadersRFCVersion
    disable_x_envoy_ratelimited_header: bool
    rate_limited_status: _http_status_pb2.HttpStatus
    response_headers_to_add: _containers.RepeatedCompositeFieldContainer[_base_pb2.HeaderValueOption]
    status_on_error: _http_status_pb2.HttpStatus
    stat_prefix: str
    def __init__(self, domain: _Optional[str] = ..., stage: _Optional[int] = ..., request_type: _Optional[str] = ..., timeout: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., failure_mode_deny: bool = ..., rate_limited_as_resource_exhausted: bool = ..., rate_limit_service: _Optional[_Union[_rls_pb2.RateLimitServiceConfig, _Mapping]] = ..., enable_x_ratelimit_headers: _Optional[_Union[RateLimit.XRateLimitHeadersRFCVersion, str]] = ..., disable_x_envoy_ratelimited_header: bool = ..., rate_limited_status: _Optional[_Union[_http_status_pb2.HttpStatus, _Mapping]] = ..., response_headers_to_add: _Optional[_Iterable[_Union[_base_pb2.HeaderValueOption, _Mapping]]] = ..., status_on_error: _Optional[_Union[_http_status_pb2.HttpStatus, _Mapping]] = ..., stat_prefix: _Optional[str] = ...) -> None: ...

class RateLimitConfig(_message.Message):
    __slots__ = ("stage", "disable_key", "actions", "limit")
    class Action(_message.Message):
        __slots__ = ("source_cluster", "destination_cluster", "request_headers", "remote_address", "generic_key", "header_value_match", "metadata", "extension")
        class SourceCluster(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        class DestinationCluster(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        class RequestHeaders(_message.Message):
            __slots__ = ("header_name", "descriptor_key", "skip_if_absent")
            HEADER_NAME_FIELD_NUMBER: _ClassVar[int]
            DESCRIPTOR_KEY_FIELD_NUMBER: _ClassVar[int]
            SKIP_IF_ABSENT_FIELD_NUMBER: _ClassVar[int]
            header_name: str
            descriptor_key: str
            skip_if_absent: bool
            def __init__(self, header_name: _Optional[str] = ..., descriptor_key: _Optional[str] = ..., skip_if_absent: bool = ...) -> None: ...
        class RemoteAddress(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        class GenericKey(_message.Message):
            __slots__ = ("descriptor_value", "descriptor_key")
            DESCRIPTOR_VALUE_FIELD_NUMBER: _ClassVar[int]
            DESCRIPTOR_KEY_FIELD_NUMBER: _ClassVar[int]
            descriptor_value: str
            descriptor_key: str
            def __init__(self, descriptor_value: _Optional[str] = ..., descriptor_key: _Optional[str] = ...) -> None: ...
        class HeaderValueMatch(_message.Message):
            __slots__ = ("descriptor_value", "expect_match", "headers")
            DESCRIPTOR_VALUE_FIELD_NUMBER: _ClassVar[int]
            EXPECT_MATCH_FIELD_NUMBER: _ClassVar[int]
            HEADERS_FIELD_NUMBER: _ClassVar[int]
            descriptor_value: str
            expect_match: bool
            headers: _containers.RepeatedCompositeFieldContainer[_route_components_pb2.HeaderMatcher]
            def __init__(self, descriptor_value: _Optional[str] = ..., expect_match: bool = ..., headers: _Optional[_Iterable[_Union[_route_components_pb2.HeaderMatcher, _Mapping]]] = ...) -> None: ...
        class MetaData(_message.Message):
            __slots__ = ("descriptor_key", "metadata_key", "default_value", "source", "skip_if_absent")
            class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                DYNAMIC: _ClassVar[RateLimitConfig.Action.MetaData.Source]
                ROUTE_ENTRY: _ClassVar[RateLimitConfig.Action.MetaData.Source]
            DYNAMIC: RateLimitConfig.Action.MetaData.Source
            ROUTE_ENTRY: RateLimitConfig.Action.MetaData.Source
            DESCRIPTOR_KEY_FIELD_NUMBER: _ClassVar[int]
            METADATA_KEY_FIELD_NUMBER: _ClassVar[int]
            DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
            SOURCE_FIELD_NUMBER: _ClassVar[int]
            SKIP_IF_ABSENT_FIELD_NUMBER: _ClassVar[int]
            descriptor_key: str
            metadata_key: _metadata_pb2.MetadataKey
            default_value: str
            source: RateLimitConfig.Action.MetaData.Source
            skip_if_absent: bool
            def __init__(self, descriptor_key: _Optional[str] = ..., metadata_key: _Optional[_Union[_metadata_pb2.MetadataKey, _Mapping]] = ..., default_value: _Optional[str] = ..., source: _Optional[_Union[RateLimitConfig.Action.MetaData.Source, str]] = ..., skip_if_absent: bool = ...) -> None: ...
        SOURCE_CLUSTER_FIELD_NUMBER: _ClassVar[int]
        DESTINATION_CLUSTER_FIELD_NUMBER: _ClassVar[int]
        REQUEST_HEADERS_FIELD_NUMBER: _ClassVar[int]
        REMOTE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
        GENERIC_KEY_FIELD_NUMBER: _ClassVar[int]
        HEADER_VALUE_MATCH_FIELD_NUMBER: _ClassVar[int]
        METADATA_FIELD_NUMBER: _ClassVar[int]
        EXTENSION_FIELD_NUMBER: _ClassVar[int]
        source_cluster: RateLimitConfig.Action.SourceCluster
        destination_cluster: RateLimitConfig.Action.DestinationCluster
        request_headers: RateLimitConfig.Action.RequestHeaders
        remote_address: RateLimitConfig.Action.RemoteAddress
        generic_key: RateLimitConfig.Action.GenericKey
        header_value_match: RateLimitConfig.Action.HeaderValueMatch
        metadata: RateLimitConfig.Action.MetaData
        extension: _extension_pb2.TypedExtensionConfig
        def __init__(self, source_cluster: _Optional[_Union[RateLimitConfig.Action.SourceCluster, _Mapping]] = ..., destination_cluster: _Optional[_Union[RateLimitConfig.Action.DestinationCluster, _Mapping]] = ..., request_headers: _Optional[_Union[RateLimitConfig.Action.RequestHeaders, _Mapping]] = ..., remote_address: _Optional[_Union[RateLimitConfig.Action.RemoteAddress, _Mapping]] = ..., generic_key: _Optional[_Union[RateLimitConfig.Action.GenericKey, _Mapping]] = ..., header_value_match: _Optional[_Union[RateLimitConfig.Action.HeaderValueMatch, _Mapping]] = ..., metadata: _Optional[_Union[RateLimitConfig.Action.MetaData, _Mapping]] = ..., extension: _Optional[_Union[_extension_pb2.TypedExtensionConfig, _Mapping]] = ...) -> None: ...
    class Override(_message.Message):
        __slots__ = ("dynamic_metadata",)
        class DynamicMetadata(_message.Message):
            __slots__ = ("metadata_key",)
            METADATA_KEY_FIELD_NUMBER: _ClassVar[int]
            metadata_key: _metadata_pb2.MetadataKey
            def __init__(self, metadata_key: _Optional[_Union[_metadata_pb2.MetadataKey, _Mapping]] = ...) -> None: ...
        DYNAMIC_METADATA_FIELD_NUMBER: _ClassVar[int]
        dynamic_metadata: RateLimitConfig.Override.DynamicMetadata
        def __init__(self, dynamic_metadata: _Optional[_Union[RateLimitConfig.Override.DynamicMetadata, _Mapping]] = ...) -> None: ...
    STAGE_FIELD_NUMBER: _ClassVar[int]
    DISABLE_KEY_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    stage: int
    disable_key: str
    actions: _containers.RepeatedCompositeFieldContainer[RateLimitConfig.Action]
    limit: RateLimitConfig.Override
    def __init__(self, stage: _Optional[int] = ..., disable_key: _Optional[str] = ..., actions: _Optional[_Iterable[_Union[RateLimitConfig.Action, _Mapping]]] = ..., limit: _Optional[_Union[RateLimitConfig.Override, _Mapping]] = ...) -> None: ...

class RateLimitPerRoute(_message.Message):
    __slots__ = ("vh_rate_limits", "override_option", "rate_limits", "domain")
    class VhRateLimitsOptions(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OVERRIDE: _ClassVar[RateLimitPerRoute.VhRateLimitsOptions]
        INCLUDE: _ClassVar[RateLimitPerRoute.VhRateLimitsOptions]
        IGNORE: _ClassVar[RateLimitPerRoute.VhRateLimitsOptions]
    OVERRIDE: RateLimitPerRoute.VhRateLimitsOptions
    INCLUDE: RateLimitPerRoute.VhRateLimitsOptions
    IGNORE: RateLimitPerRoute.VhRateLimitsOptions
    class OverrideOptions(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEFAULT: _ClassVar[RateLimitPerRoute.OverrideOptions]
        OVERRIDE_POLICY: _ClassVar[RateLimitPerRoute.OverrideOptions]
        INCLUDE_POLICY: _ClassVar[RateLimitPerRoute.OverrideOptions]
        IGNORE_POLICY: _ClassVar[RateLimitPerRoute.OverrideOptions]
    DEFAULT: RateLimitPerRoute.OverrideOptions
    OVERRIDE_POLICY: RateLimitPerRoute.OverrideOptions
    INCLUDE_POLICY: RateLimitPerRoute.OverrideOptions
    IGNORE_POLICY: RateLimitPerRoute.OverrideOptions
    VH_RATE_LIMITS_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_OPTION_FIELD_NUMBER: _ClassVar[int]
    RATE_LIMITS_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    vh_rate_limits: RateLimitPerRoute.VhRateLimitsOptions
    override_option: RateLimitPerRoute.OverrideOptions
    rate_limits: _containers.RepeatedCompositeFieldContainer[RateLimitConfig]
    domain: str
    def __init__(self, vh_rate_limits: _Optional[_Union[RateLimitPerRoute.VhRateLimitsOptions, str]] = ..., override_option: _Optional[_Union[RateLimitPerRoute.OverrideOptions, str]] = ..., rate_limits: _Optional[_Iterable[_Union[RateLimitConfig, _Mapping]]] = ..., domain: _Optional[str] = ...) -> None: ...
