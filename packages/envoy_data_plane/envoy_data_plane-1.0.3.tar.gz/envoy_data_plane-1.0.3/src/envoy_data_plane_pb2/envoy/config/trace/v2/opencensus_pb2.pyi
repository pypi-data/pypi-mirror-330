from envoy.api.v2.core import grpc_service_pb2 as _grpc_service_pb2
from opencensus.proto.trace.v1 import trace_config_pb2 as _trace_config_pb2
from udpa.annotations import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpenCensusConfig(_message.Message):
    __slots__ = ("trace_config", "stdout_exporter_enabled", "stackdriver_exporter_enabled", "stackdriver_project_id", "stackdriver_address", "stackdriver_grpc_service", "zipkin_exporter_enabled", "zipkin_url", "ocagent_exporter_enabled", "ocagent_address", "ocagent_grpc_service", "incoming_trace_context", "outgoing_trace_context")
    class TraceContext(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NONE: _ClassVar[OpenCensusConfig.TraceContext]
        TRACE_CONTEXT: _ClassVar[OpenCensusConfig.TraceContext]
        GRPC_TRACE_BIN: _ClassVar[OpenCensusConfig.TraceContext]
        CLOUD_TRACE_CONTEXT: _ClassVar[OpenCensusConfig.TraceContext]
        B3: _ClassVar[OpenCensusConfig.TraceContext]
    NONE: OpenCensusConfig.TraceContext
    TRACE_CONTEXT: OpenCensusConfig.TraceContext
    GRPC_TRACE_BIN: OpenCensusConfig.TraceContext
    CLOUD_TRACE_CONTEXT: OpenCensusConfig.TraceContext
    B3: OpenCensusConfig.TraceContext
    TRACE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    STDOUT_EXPORTER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    STACKDRIVER_EXPORTER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    STACKDRIVER_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    STACKDRIVER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    STACKDRIVER_GRPC_SERVICE_FIELD_NUMBER: _ClassVar[int]
    ZIPKIN_EXPORTER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ZIPKIN_URL_FIELD_NUMBER: _ClassVar[int]
    OCAGENT_EXPORTER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    OCAGENT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    OCAGENT_GRPC_SERVICE_FIELD_NUMBER: _ClassVar[int]
    INCOMING_TRACE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    OUTGOING_TRACE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    trace_config: _trace_config_pb2.TraceConfig
    stdout_exporter_enabled: bool
    stackdriver_exporter_enabled: bool
    stackdriver_project_id: str
    stackdriver_address: str
    stackdriver_grpc_service: _grpc_service_pb2.GrpcService
    zipkin_exporter_enabled: bool
    zipkin_url: str
    ocagent_exporter_enabled: bool
    ocagent_address: str
    ocagent_grpc_service: _grpc_service_pb2.GrpcService
    incoming_trace_context: _containers.RepeatedScalarFieldContainer[OpenCensusConfig.TraceContext]
    outgoing_trace_context: _containers.RepeatedScalarFieldContainer[OpenCensusConfig.TraceContext]
    def __init__(self, trace_config: _Optional[_Union[_trace_config_pb2.TraceConfig, _Mapping]] = ..., stdout_exporter_enabled: bool = ..., stackdriver_exporter_enabled: bool = ..., stackdriver_project_id: _Optional[str] = ..., stackdriver_address: _Optional[str] = ..., stackdriver_grpc_service: _Optional[_Union[_grpc_service_pb2.GrpcService, _Mapping]] = ..., zipkin_exporter_enabled: bool = ..., zipkin_url: _Optional[str] = ..., ocagent_exporter_enabled: bool = ..., ocagent_address: _Optional[str] = ..., ocagent_grpc_service: _Optional[_Union[_grpc_service_pb2.GrpcService, _Mapping]] = ..., incoming_trace_context: _Optional[_Iterable[_Union[OpenCensusConfig.TraceContext, str]]] = ..., outgoing_trace_context: _Optional[_Iterable[_Union[OpenCensusConfig.TraceContext, str]]] = ...) -> None: ...
