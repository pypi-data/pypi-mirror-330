from envoy.config.core.v3 import grpc_service_pb2 as _grpc_service_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from udpa.annotations import status_pb2 as _status_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SinkConfig(_message.Message):
    __slots__ = ("grpc_service", "report_counters_as_deltas", "report_histograms_as_deltas", "emit_tags_as_attributes", "use_tag_extracted_name", "prefix")
    GRPC_SERVICE_FIELD_NUMBER: _ClassVar[int]
    REPORT_COUNTERS_AS_DELTAS_FIELD_NUMBER: _ClassVar[int]
    REPORT_HISTOGRAMS_AS_DELTAS_FIELD_NUMBER: _ClassVar[int]
    EMIT_TAGS_AS_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    USE_TAG_EXTRACTED_NAME_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    grpc_service: _grpc_service_pb2.GrpcService
    report_counters_as_deltas: bool
    report_histograms_as_deltas: bool
    emit_tags_as_attributes: _wrappers_pb2.BoolValue
    use_tag_extracted_name: _wrappers_pb2.BoolValue
    prefix: str
    def __init__(self, grpc_service: _Optional[_Union[_grpc_service_pb2.GrpcService, _Mapping]] = ..., report_counters_as_deltas: bool = ..., report_histograms_as_deltas: bool = ..., emit_tags_as_attributes: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., use_tag_extracted_name: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., prefix: _Optional[str] = ...) -> None: ...
