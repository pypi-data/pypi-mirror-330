from protobuf import shared_pb2 as _shared_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IfDataType(_message.Message):
    __slots__ = ("Name", "Blob")
    NAME_FIELD_NUMBER: _ClassVar[int]
    BLOB_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    Blob: _containers.RepeatedCompositeFieldContainer[GenericParameterType]
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., Blob: _Optional[_Iterable[_Union[GenericParameterType, _Mapping]]] = ...) -> None: ...

class GenericParameterType(_message.Message):
    __slots__ = ("Tag", "String", "Long", "Float", "Generic", "Identifier")
    TAG_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    LONG_FIELD_NUMBER: _ClassVar[int]
    FLOAT_FIELD_NUMBER: _ClassVar[int]
    GENERIC_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Tag: _shared_pb2.TagType
    String: _shared_pb2.StringType
    Long: _shared_pb2.LongType
    Float: _shared_pb2.FloatType
    Generic: GenericNodeType
    Identifier: _shared_pb2.IdentType
    def __init__(self, Tag: _Optional[_Union[_shared_pb2.TagType, _Mapping]] = ..., String: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Long: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ..., Float: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., Generic: _Optional[_Union[GenericNodeType, _Mapping]] = ..., Identifier: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class GenericNodeType(_message.Message):
    __slots__ = ("Name", "Element")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ELEMENT_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    Element: _containers.RepeatedCompositeFieldContainer[GenericParameterType]
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., Element: _Optional[_Iterable[_Union[GenericParameterType, _Mapping]]] = ...) -> None: ...
