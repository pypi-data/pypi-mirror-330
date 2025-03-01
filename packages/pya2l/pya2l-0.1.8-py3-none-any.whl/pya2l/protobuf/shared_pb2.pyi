from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IntType(_message.Message):
    __slots__ = ("Value", "Base", "Size")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    Value: int
    Base: int
    Size: int
    def __init__(self, Value: _Optional[int] = ..., Base: _Optional[int] = ..., Size: _Optional[int] = ...) -> None: ...

class LongType(_message.Message):
    __slots__ = ("Value", "Base", "Size")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    Value: int
    Base: int
    Size: int
    def __init__(self, Value: _Optional[int] = ..., Base: _Optional[int] = ..., Size: _Optional[int] = ...) -> None: ...

class FloatType(_message.Message):
    __slots__ = ("Value", "IntegralSign", "IntegralSize", "DecimalSize", "ExponentSign", "ExponentSize")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    INTEGRALSIGN_FIELD_NUMBER: _ClassVar[int]
    INTEGRALSIZE_FIELD_NUMBER: _ClassVar[int]
    DECIMALSIZE_FIELD_NUMBER: _ClassVar[int]
    EXPONENTSIGN_FIELD_NUMBER: _ClassVar[int]
    EXPONENTSIZE_FIELD_NUMBER: _ClassVar[int]
    Value: float
    IntegralSign: str
    IntegralSize: int
    DecimalSize: int
    ExponentSign: str
    ExponentSize: int
    def __init__(self, Value: _Optional[float] = ..., IntegralSign: _Optional[str] = ..., IntegralSize: _Optional[int] = ..., DecimalSize: _Optional[int] = ..., ExponentSign: _Optional[str] = ..., ExponentSize: _Optional[int] = ...) -> None: ...

class IdentType(_message.Message):
    __slots__ = ("Value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    Value: str
    def __init__(self, Value: _Optional[str] = ...) -> None: ...

class StringType(_message.Message):
    __slots__ = ("Value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    Value: str
    def __init__(self, Value: _Optional[str] = ...) -> None: ...

class TagType(_message.Message):
    __slots__ = ("Value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    Value: str
    def __init__(self, Value: _Optional[str] = ...) -> None: ...
