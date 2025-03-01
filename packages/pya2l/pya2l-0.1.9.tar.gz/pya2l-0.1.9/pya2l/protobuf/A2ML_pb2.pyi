from protobuf import shared_pb2 as _shared_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class declaration(_message.Message):
    __slots__ = ("type_definition", "block_definition")
    TYPE_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    BLOCK_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    type_definition: type_definition
    block_definition: block_definition
    def __init__(self, type_definition: _Optional[_Union[type_definition, _Mapping]] = ..., block_definition: _Optional[_Union[block_definition, _Mapping]] = ...) -> None: ...

class type_definition(_message.Message):
    __slots__ = ("type_name",)
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    type_name: type_name
    def __init__(self, type_name: _Optional[_Union[type_name, _Mapping]] = ...) -> None: ...

class type_name(_message.Message):
    __slots__ = ("predefined_type_name", "struct_type_name", "taggedstruct_type_name", "taggedunion_type_name", "enum_type_name")
    PREDEFINED_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    STRUCT_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    TAGGEDSTRUCT_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    TAGGEDUNION_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENUM_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    predefined_type_name: predefined_type_name
    struct_type_name: struct_type_name
    taggedstruct_type_name: taggedstruct_type_name
    taggedunion_type_name: taggedunion_type_name
    enum_type_name: enum_type_name
    def __init__(self, predefined_type_name: _Optional[_Union[predefined_type_name, _Mapping]] = ..., struct_type_name: _Optional[_Union[struct_type_name, _Mapping]] = ..., taggedstruct_type_name: _Optional[_Union[taggedstruct_type_name, _Mapping]] = ..., taggedunion_type_name: _Optional[_Union[taggedunion_type_name, _Mapping]] = ..., enum_type_name: _Optional[_Union[enum_type_name, _Mapping]] = ...) -> None: ...

class predefined_type_name(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class block_definition(_message.Message):
    __slots__ = ("tag", "type_name", "member")
    TAG_FIELD_NUMBER: _ClassVar[int]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    tag: _shared_pb2.TagType
    type_name: type_name
    member: member
    def __init__(self, tag: _Optional[_Union[_shared_pb2.TagType, _Mapping]] = ..., type_name: _Optional[_Union[type_name, _Mapping]] = ..., member: _Optional[_Union[member, _Mapping]] = ...) -> None: ...

class enum_type_name(_message.Message):
    __slots__ = ("identifier", "enumerator_list")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ENUMERATOR_LIST_FIELD_NUMBER: _ClassVar[int]
    identifier: _shared_pb2.IdentType
    enumerator_list: _containers.RepeatedCompositeFieldContainer[enumerator]
    def __init__(self, identifier: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., enumerator_list: _Optional[_Iterable[_Union[enumerator, _Mapping]]] = ...) -> None: ...

class enumerator(_message.Message):
    __slots__ = ("keyword", "constant")
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    CONSTANT_FIELD_NUMBER: _ClassVar[int]
    keyword: _shared_pb2.StringType
    constant: _shared_pb2.LongType
    def __init__(self, keyword: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., constant: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ...) -> None: ...

class struct_type_name(_message.Message):
    __slots__ = ("identifier", "struct_member_list")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    STRUCT_MEMBER_LIST_FIELD_NUMBER: _ClassVar[int]
    identifier: _shared_pb2.IdentType
    struct_member_list: _containers.RepeatedCompositeFieldContainer[struct_member]
    def __init__(self, identifier: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., struct_member_list: _Optional[_Iterable[_Union[struct_member, _Mapping]]] = ...) -> None: ...

class struct_member(_message.Message):
    __slots__ = ("member", "star")
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    STAR_FIELD_NUMBER: _ClassVar[int]
    member: member
    star: bool
    def __init__(self, member: _Optional[_Union[member, _Mapping]] = ..., star: bool = ...) -> None: ...

class member(_message.Message):
    __slots__ = ("type_name", "array_specifier")
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    ARRAY_SPECIFIER_FIELD_NUMBER: _ClassVar[int]
    type_name: type_name
    array_specifier: array_specifier
    def __init__(self, type_name: _Optional[_Union[type_name, _Mapping]] = ..., array_specifier: _Optional[_Union[array_specifier, _Mapping]] = ...) -> None: ...

class array_specifier(_message.Message):
    __slots__ = ("constant",)
    CONSTANT_FIELD_NUMBER: _ClassVar[int]
    constant: _containers.RepeatedCompositeFieldContainer[_shared_pb2.LongType]
    def __init__(self, constant: _Optional[_Iterable[_Union[_shared_pb2.LongType, _Mapping]]] = ...) -> None: ...

class taggedstruct_type_name(_message.Message):
    __slots__ = ("identifier", "taggedstruct_member_list")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    TAGGEDSTRUCT_MEMBER_LIST_FIELD_NUMBER: _ClassVar[int]
    identifier: _shared_pb2.IdentType
    taggedstruct_member_list: _containers.RepeatedCompositeFieldContainer[taggedstruct_member]
    def __init__(self, identifier: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., taggedstruct_member_list: _Optional[_Iterable[_Union[taggedstruct_member, _Mapping]]] = ...) -> None: ...

class taggedstruct_member(_message.Message):
    __slots__ = ("taggedstruct_definition", "block_definition", "star")
    TAGGEDSTRUCT_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    BLOCK_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    STAR_FIELD_NUMBER: _ClassVar[int]
    taggedstruct_definition: taggedstruct_definition
    block_definition: block_definition
    star: bool
    def __init__(self, taggedstruct_definition: _Optional[_Union[taggedstruct_definition, _Mapping]] = ..., block_definition: _Optional[_Union[block_definition, _Mapping]] = ..., star: bool = ...) -> None: ...

class taggedstruct_definition(_message.Message):
    __slots__ = ("tag", "member", "star")
    TAG_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    STAR_FIELD_NUMBER: _ClassVar[int]
    tag: _shared_pb2.TagType
    member: member
    star: bool
    def __init__(self, tag: _Optional[_Union[_shared_pb2.TagType, _Mapping]] = ..., member: _Optional[_Union[member, _Mapping]] = ..., star: bool = ...) -> None: ...

class taggedunion_type_name(_message.Message):
    __slots__ = ("identifier", "taggedunion_member_list")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    TAGGEDUNION_MEMBER_LIST_FIELD_NUMBER: _ClassVar[int]
    identifier: _shared_pb2.IdentType
    taggedunion_member_list: _containers.RepeatedCompositeFieldContainer[taggedunion_member]
    def __init__(self, identifier: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., taggedunion_member_list: _Optional[_Iterable[_Union[taggedunion_member, _Mapping]]] = ...) -> None: ...

class taggedunion_member(_message.Message):
    __slots__ = ("tag_member", "block_definition")
    TAG_MEMBER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    tag_member: tag_member
    block_definition: block_definition
    def __init__(self, tag_member: _Optional[_Union[tag_member, _Mapping]] = ..., block_definition: _Optional[_Union[block_definition, _Mapping]] = ...) -> None: ...

class tag_member(_message.Message):
    __slots__ = ("tag", "member")
    TAG_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    tag: _shared_pb2.TagType
    member: member
    def __init__(self, tag: _Optional[_Union[_shared_pb2.TagType, _Mapping]] = ..., member: _Optional[_Union[member, _Mapping]] = ...) -> None: ...
