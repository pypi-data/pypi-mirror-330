from envoy.config.common.mutation_rules.v3 import mutation_rules_pb2 as _mutation_rules_pb2
from udpa.annotations import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Mutations(_message.Message):
    __slots__ = ("request_mutations", "response_mutations")
    REQUEST_MUTATIONS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_MUTATIONS_FIELD_NUMBER: _ClassVar[int]
    request_mutations: _containers.RepeatedCompositeFieldContainer[_mutation_rules_pb2.HeaderMutation]
    response_mutations: _containers.RepeatedCompositeFieldContainer[_mutation_rules_pb2.HeaderMutation]
    def __init__(self, request_mutations: _Optional[_Iterable[_Union[_mutation_rules_pb2.HeaderMutation, _Mapping]]] = ..., response_mutations: _Optional[_Iterable[_Union[_mutation_rules_pb2.HeaderMutation, _Mapping]]] = ...) -> None: ...

class HeaderMutationPerRoute(_message.Message):
    __slots__ = ("mutations",)
    MUTATIONS_FIELD_NUMBER: _ClassVar[int]
    mutations: Mutations
    def __init__(self, mutations: _Optional[_Union[Mutations, _Mapping]] = ...) -> None: ...

class HeaderMutation(_message.Message):
    __slots__ = ("mutations", "most_specific_header_mutations_wins")
    MUTATIONS_FIELD_NUMBER: _ClassVar[int]
    MOST_SPECIFIC_HEADER_MUTATIONS_WINS_FIELD_NUMBER: _ClassVar[int]
    mutations: Mutations
    most_specific_header_mutations_wins: bool
    def __init__(self, mutations: _Optional[_Union[Mutations, _Mapping]] = ..., most_specific_header_mutations_wins: bool = ...) -> None: ...
