from udpa.annotations import status_pb2 as _status_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProxyProtocolPassThroughTLVs(_message.Message):
    __slots__ = ("match_type", "tlv_type")
    class PassTLVsMatchType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INCLUDE_ALL: _ClassVar[ProxyProtocolPassThroughTLVs.PassTLVsMatchType]
        INCLUDE: _ClassVar[ProxyProtocolPassThroughTLVs.PassTLVsMatchType]
    INCLUDE_ALL: ProxyProtocolPassThroughTLVs.PassTLVsMatchType
    INCLUDE: ProxyProtocolPassThroughTLVs.PassTLVsMatchType
    MATCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    TLV_TYPE_FIELD_NUMBER: _ClassVar[int]
    match_type: ProxyProtocolPassThroughTLVs.PassTLVsMatchType
    tlv_type: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, match_type: _Optional[_Union[ProxyProtocolPassThroughTLVs.PassTLVsMatchType, str]] = ..., tlv_type: _Optional[_Iterable[int]] = ...) -> None: ...

class ProxyProtocolConfig(_message.Message):
    __slots__ = ("version", "pass_through_tlvs")
    class Version(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        V1: _ClassVar[ProxyProtocolConfig.Version]
        V2: _ClassVar[ProxyProtocolConfig.Version]
    V1: ProxyProtocolConfig.Version
    V2: ProxyProtocolConfig.Version
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PASS_THROUGH_TLVS_FIELD_NUMBER: _ClassVar[int]
    version: ProxyProtocolConfig.Version
    pass_through_tlvs: ProxyProtocolPassThroughTLVs
    def __init__(self, version: _Optional[_Union[ProxyProtocolConfig.Version, str]] = ..., pass_through_tlvs: _Optional[_Union[ProxyProtocolPassThroughTLVs, _Mapping]] = ...) -> None: ...
