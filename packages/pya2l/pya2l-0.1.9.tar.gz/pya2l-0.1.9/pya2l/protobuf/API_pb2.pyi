from protobuf import A2L_pb2 as _A2L_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TreeFromA2LRequest(_message.Message):
    __slots__ = ("a2l",)
    A2L_FIELD_NUMBER: _ClassVar[int]
    a2l: bytes
    def __init__(self, a2l: _Optional[bytes] = ...) -> None: ...

class A2LResponse(_message.Message):
    __slots__ = ("a2l", "error")
    A2L_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    a2l: bytes
    error: str
    def __init__(self, a2l: _Optional[bytes] = ..., error: _Optional[str] = ...) -> None: ...

class JSONFromTreeRequest(_message.Message):
    __slots__ = ("tree", "indent", "allow_partial", "emit_unpopulated")
    TREE_FIELD_NUMBER: _ClassVar[int]
    INDENT_FIELD_NUMBER: _ClassVar[int]
    ALLOW_PARTIAL_FIELD_NUMBER: _ClassVar[int]
    EMIT_UNPOPULATED_FIELD_NUMBER: _ClassVar[int]
    tree: bytes
    indent: int
    allow_partial: bool
    emit_unpopulated: bool
    def __init__(self, tree: _Optional[bytes] = ..., indent: _Optional[int] = ..., allow_partial: bool = ..., emit_unpopulated: bool = ...) -> None: ...

class A2LFromTreeRequest(_message.Message):
    __slots__ = ("tree", "indent", "sorted")
    TREE_FIELD_NUMBER: _ClassVar[int]
    INDENT_FIELD_NUMBER: _ClassVar[int]
    SORTED_FIELD_NUMBER: _ClassVar[int]
    tree: bytes
    indent: int
    sorted: bool
    def __init__(self, tree: _Optional[bytes] = ..., indent: _Optional[int] = ..., sorted: bool = ...) -> None: ...

class TreeResponse(_message.Message):
    __slots__ = ("serializedTreeChunk", "error")
    SERIALIZEDTREECHUNK_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    serializedTreeChunk: bytes
    error: str
    def __init__(self, serializedTreeChunk: _Optional[bytes] = ..., error: _Optional[str] = ...) -> None: ...

class TreeFromJSONRequest(_message.Message):
    __slots__ = ("json", "allow_partial")
    JSON_FIELD_NUMBER: _ClassVar[int]
    ALLOW_PARTIAL_FIELD_NUMBER: _ClassVar[int]
    json: bytes
    allow_partial: bool
    def __init__(self, json: _Optional[bytes] = ..., allow_partial: bool = ...) -> None: ...

class JSONResponse(_message.Message):
    __slots__ = ("json", "error")
    JSON_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    json: bytes
    error: str
    def __init__(self, json: _Optional[bytes] = ..., error: _Optional[str] = ...) -> None: ...
