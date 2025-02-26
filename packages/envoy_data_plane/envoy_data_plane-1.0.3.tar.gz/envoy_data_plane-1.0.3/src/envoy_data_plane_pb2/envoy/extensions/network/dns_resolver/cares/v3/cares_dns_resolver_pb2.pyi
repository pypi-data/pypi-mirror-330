from envoy.config.core.v3 import address_pb2 as _address_pb2
from envoy.config.core.v3 import resolver_pb2 as _resolver_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from udpa.annotations import status_pb2 as _status_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CaresDnsResolverConfig(_message.Message):
    __slots__ = ("resolvers", "use_resolvers_as_fallback", "filter_unroutable_families", "dns_resolver_options", "udp_max_queries")
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    USE_RESOLVERS_AS_FALLBACK_FIELD_NUMBER: _ClassVar[int]
    FILTER_UNROUTABLE_FAMILIES_FIELD_NUMBER: _ClassVar[int]
    DNS_RESOLVER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    UDP_MAX_QUERIES_FIELD_NUMBER: _ClassVar[int]
    resolvers: _containers.RepeatedCompositeFieldContainer[_address_pb2.Address]
    use_resolvers_as_fallback: bool
    filter_unroutable_families: bool
    dns_resolver_options: _resolver_pb2.DnsResolverOptions
    udp_max_queries: _wrappers_pb2.UInt32Value
    def __init__(self, resolvers: _Optional[_Iterable[_Union[_address_pb2.Address, _Mapping]]] = ..., use_resolvers_as_fallback: bool = ..., filter_unroutable_families: bool = ..., dns_resolver_options: _Optional[_Union[_resolver_pb2.DnsResolverOptions, _Mapping]] = ..., udp_max_queries: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ...) -> None: ...
