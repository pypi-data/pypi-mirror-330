from protobuf import A2ML_pb2 as _A2ML_pb2
from protobuf import IF_DATA_pb2 as _IF_DATA_pb2
from protobuf import shared_pb2 as _shared_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddrTypeType(_message.Message):
    __slots__ = ("Value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    Value: str
    def __init__(self, Value: _Optional[str] = ...) -> None: ...

class DataTypeType(_message.Message):
    __slots__ = ("Value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    Value: str
    def __init__(self, Value: _Optional[str] = ...) -> None: ...

class IndexOrderType(_message.Message):
    __slots__ = ("Value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    Value: str
    def __init__(self, Value: _Optional[str] = ...) -> None: ...

class A2MLType(_message.Message):
    __slots__ = ("Declaration",)
    DECLARATION_FIELD_NUMBER: _ClassVar[int]
    Declaration: _containers.RepeatedCompositeFieldContainer[_A2ML_pb2.declaration]
    def __init__(self, Declaration: _Optional[_Iterable[_Union[_A2ML_pb2.declaration, _Mapping]]] = ...) -> None: ...

class A2MLVersionType(_message.Message):
    __slots__ = ("VersionNo", "UpgradeNo")
    VERSIONNO_FIELD_NUMBER: _ClassVar[int]
    UPGRADENO_FIELD_NUMBER: _ClassVar[int]
    VersionNo: _shared_pb2.IntType
    UpgradeNo: _shared_pb2.IntType
    def __init__(self, VersionNo: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., UpgradeNo: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class AddrEpkType(_message.Message):
    __slots__ = ("Address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    Address: _shared_pb2.LongType
    def __init__(self, Address: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ...) -> None: ...

class AlignmentByteType(_message.Message):
    __slots__ = ("AlignmentBorder",)
    ALIGNMENTBORDER_FIELD_NUMBER: _ClassVar[int]
    AlignmentBorder: _shared_pb2.IntType
    def __init__(self, AlignmentBorder: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class AlignmentFloat32IeeeType(_message.Message):
    __slots__ = ("AlignmentBorder",)
    ALIGNMENTBORDER_FIELD_NUMBER: _ClassVar[int]
    AlignmentBorder: _shared_pb2.IntType
    def __init__(self, AlignmentBorder: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class AlignmentFloat64IeeeType(_message.Message):
    __slots__ = ("AlignmentBorder",)
    ALIGNMENTBORDER_FIELD_NUMBER: _ClassVar[int]
    AlignmentBorder: _shared_pb2.IntType
    def __init__(self, AlignmentBorder: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class AlignmentLongType(_message.Message):
    __slots__ = ("AlignmentBorder",)
    ALIGNMENTBORDER_FIELD_NUMBER: _ClassVar[int]
    AlignmentBorder: _shared_pb2.IntType
    def __init__(self, AlignmentBorder: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class AlignmentWordType(_message.Message):
    __slots__ = ("AlignmentBorder",)
    ALIGNMENTBORDER_FIELD_NUMBER: _ClassVar[int]
    AlignmentBorder: _shared_pb2.IntType
    def __init__(self, AlignmentBorder: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class AnnotationLabelType(_message.Message):
    __slots__ = ("Label",)
    LABEL_FIELD_NUMBER: _ClassVar[int]
    Label: _shared_pb2.StringType
    def __init__(self, Label: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class AnnotationOriginType(_message.Message):
    __slots__ = ("Origin",)
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    Origin: _shared_pb2.StringType
    def __init__(self, Origin: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class AnnotationTextType(_message.Message):
    __slots__ = ("AnnotationText",)
    ANNOTATIONTEXT_FIELD_NUMBER: _ClassVar[int]
    AnnotationText: _containers.RepeatedCompositeFieldContainer[_shared_pb2.StringType]
    def __init__(self, AnnotationText: _Optional[_Iterable[_Union[_shared_pb2.StringType, _Mapping]]] = ...) -> None: ...

class AnnotationType(_message.Message):
    __slots__ = ("ANNOTATION_LABEL", "ANNOTATION_ORIGIN", "ANNOTATION_TEXT")
    ANNOTATION_LABEL_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_TEXT_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_LABEL: AnnotationLabelType
    ANNOTATION_ORIGIN: AnnotationOriginType
    ANNOTATION_TEXT: AnnotationTextType
    def __init__(self, ANNOTATION_LABEL: _Optional[_Union[AnnotationLabelType, _Mapping]] = ..., ANNOTATION_ORIGIN: _Optional[_Union[AnnotationOriginType, _Mapping]] = ..., ANNOTATION_TEXT: _Optional[_Union[AnnotationTextType, _Mapping]] = ...) -> None: ...

class ArraySizeType(_message.Message):
    __slots__ = ("Number",)
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    Number: _shared_pb2.IntType
    def __init__(self, Number: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class ASAP2VersionType(_message.Message):
    __slots__ = ("VersionNo", "UpgradeNo")
    VERSIONNO_FIELD_NUMBER: _ClassVar[int]
    UPGRADENO_FIELD_NUMBER: _ClassVar[int]
    VersionNo: _shared_pb2.IntType
    UpgradeNo: _shared_pb2.IntType
    def __init__(self, VersionNo: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., UpgradeNo: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class AxisDescrType(_message.Message):
    __slots__ = ("Attribute", "InputQuantity", "Conversion", "MaxAxisPoints", "LowerLimit", "UpperLimit", "READ_ONLY", "FORMAT", "ANNOTATION", "AXIS_PTS_REF", "MAX_GRAD", "MONOTONY", "BYTE_ORDER", "EXTENDED_LIMITS", "FIX_AXIS_PAR", "FIX_AXIS_PAR_DIST", "FIX_AXIS_PAR_LIST", "DEPOSIT", "CURVE_AXIS_REF", "STEP_SIZE", "PHYS_UNIT")
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    INPUTQUANTITY_FIELD_NUMBER: _ClassVar[int]
    CONVERSION_FIELD_NUMBER: _ClassVar[int]
    MAXAXISPOINTS_FIELD_NUMBER: _ClassVar[int]
    LOWERLIMIT_FIELD_NUMBER: _ClassVar[int]
    UPPERLIMIT_FIELD_NUMBER: _ClassVar[int]
    READ_ONLY_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_FIELD_NUMBER: _ClassVar[int]
    AXIS_PTS_REF_FIELD_NUMBER: _ClassVar[int]
    MAX_GRAD_FIELD_NUMBER: _ClassVar[int]
    MONOTONY_FIELD_NUMBER: _ClassVar[int]
    BYTE_ORDER_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_LIMITS_FIELD_NUMBER: _ClassVar[int]
    FIX_AXIS_PAR_FIELD_NUMBER: _ClassVar[int]
    FIX_AXIS_PAR_DIST_FIELD_NUMBER: _ClassVar[int]
    FIX_AXIS_PAR_LIST_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    CURVE_AXIS_REF_FIELD_NUMBER: _ClassVar[int]
    STEP_SIZE_FIELD_NUMBER: _ClassVar[int]
    PHYS_UNIT_FIELD_NUMBER: _ClassVar[int]
    Attribute: str
    InputQuantity: _shared_pb2.IdentType
    Conversion: _shared_pb2.IdentType
    MaxAxisPoints: _shared_pb2.IntType
    LowerLimit: _shared_pb2.FloatType
    UpperLimit: _shared_pb2.FloatType
    READ_ONLY: ReadOnlyType
    FORMAT: FormatType
    ANNOTATION: _containers.RepeatedCompositeFieldContainer[AnnotationType]
    AXIS_PTS_REF: AxisPtsRefType
    MAX_GRAD: MaxGradType
    MONOTONY: MonotonyType
    BYTE_ORDER: ByteOrderType
    EXTENDED_LIMITS: ExtendedLimitsType
    FIX_AXIS_PAR: FixAxisParType
    FIX_AXIS_PAR_DIST: FixAxisParDistType
    FIX_AXIS_PAR_LIST: FixAxisParListType
    DEPOSIT: DepositType
    CURVE_AXIS_REF: CurveAxisRefType
    STEP_SIZE: StepSizeType
    PHYS_UNIT: PhysUnitType
    def __init__(self, Attribute: _Optional[str] = ..., InputQuantity: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., Conversion: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., MaxAxisPoints: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., LowerLimit: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., UpperLimit: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., READ_ONLY: _Optional[_Union[ReadOnlyType, _Mapping]] = ..., FORMAT: _Optional[_Union[FormatType, _Mapping]] = ..., ANNOTATION: _Optional[_Iterable[_Union[AnnotationType, _Mapping]]] = ..., AXIS_PTS_REF: _Optional[_Union[AxisPtsRefType, _Mapping]] = ..., MAX_GRAD: _Optional[_Union[MaxGradType, _Mapping]] = ..., MONOTONY: _Optional[_Union[MonotonyType, _Mapping]] = ..., BYTE_ORDER: _Optional[_Union[ByteOrderType, _Mapping]] = ..., EXTENDED_LIMITS: _Optional[_Union[ExtendedLimitsType, _Mapping]] = ..., FIX_AXIS_PAR: _Optional[_Union[FixAxisParType, _Mapping]] = ..., FIX_AXIS_PAR_DIST: _Optional[_Union[FixAxisParDistType, _Mapping]] = ..., FIX_AXIS_PAR_LIST: _Optional[_Union[FixAxisParListType, _Mapping]] = ..., DEPOSIT: _Optional[_Union[DepositType, _Mapping]] = ..., CURVE_AXIS_REF: _Optional[_Union[CurveAxisRefType, _Mapping]] = ..., STEP_SIZE: _Optional[_Union[StepSizeType, _Mapping]] = ..., PHYS_UNIT: _Optional[_Union[PhysUnitType, _Mapping]] = ...) -> None: ...

class AxisPtsRefType(_message.Message):
    __slots__ = ("AxisPoints",)
    AXISPOINTS_FIELD_NUMBER: _ClassVar[int]
    AxisPoints: _shared_pb2.IdentType
    def __init__(self, AxisPoints: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class AxisPtsType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "Address", "InputQuantity", "DepositR", "MaxDiff", "Conversion", "MaxAxisPoints", "LowerLimit", "UpperLimit", "DISPLAY_IDENTIFIER", "READ_ONLY", "FORMAT", "DEPOSIT", "BYTE_ORDER", "FUNCTION_LIST", "REF_MEMORY_SEGMENT", "GUARD_RAILS", "EXTENDED_LIMITS", "ANNOTATION", "IF_DATA", "CALIBRATION_ACCESS", "ECU_ADDRESS_EXTENSION", "PHYS_UNIT", "STEP_SIZE", "SYMBOL_LINK")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    INPUTQUANTITY_FIELD_NUMBER: _ClassVar[int]
    DEPOSITR_FIELD_NUMBER: _ClassVar[int]
    MAXDIFF_FIELD_NUMBER: _ClassVar[int]
    CONVERSION_FIELD_NUMBER: _ClassVar[int]
    MAXAXISPOINTS_FIELD_NUMBER: _ClassVar[int]
    LOWERLIMIT_FIELD_NUMBER: _ClassVar[int]
    UPPERLIMIT_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    READ_ONLY_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    BYTE_ORDER_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_LIST_FIELD_NUMBER: _ClassVar[int]
    REF_MEMORY_SEGMENT_FIELD_NUMBER: _ClassVar[int]
    GUARD_RAILS_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_LIMITS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_FIELD_NUMBER: _ClassVar[int]
    IF_DATA_FIELD_NUMBER: _ClassVar[int]
    CALIBRATION_ACCESS_FIELD_NUMBER: _ClassVar[int]
    ECU_ADDRESS_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    PHYS_UNIT_FIELD_NUMBER: _ClassVar[int]
    STEP_SIZE_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_LINK_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    Address: _shared_pb2.LongType
    InputQuantity: _shared_pb2.IdentType
    DepositR: _shared_pb2.IdentType
    MaxDiff: _shared_pb2.FloatType
    Conversion: _shared_pb2.IdentType
    MaxAxisPoints: _shared_pb2.IntType
    LowerLimit: _shared_pb2.FloatType
    UpperLimit: _shared_pb2.FloatType
    DISPLAY_IDENTIFIER: DisplayIdentifierType
    READ_ONLY: ReadOnlyType
    FORMAT: FormatType
    DEPOSIT: DepositType
    BYTE_ORDER: ByteOrderType
    FUNCTION_LIST: FunctionListType
    REF_MEMORY_SEGMENT: RefMemorySegmentType
    GUARD_RAILS: GuardRailsType
    EXTENDED_LIMITS: ExtendedLimitsType
    ANNOTATION: _containers.RepeatedCompositeFieldContainer[AnnotationType]
    IF_DATA: _containers.RepeatedCompositeFieldContainer[_IF_DATA_pb2.IfDataType]
    CALIBRATION_ACCESS: CalibrationAccessType
    ECU_ADDRESS_EXTENSION: EcuAddressExtensionType
    PHYS_UNIT: PhysUnitType
    STEP_SIZE: StepSizeType
    SYMBOL_LINK: SymbolLinkType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Address: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ..., InputQuantity: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., DepositR: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., MaxDiff: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., Conversion: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., MaxAxisPoints: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., LowerLimit: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., UpperLimit: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., DISPLAY_IDENTIFIER: _Optional[_Union[DisplayIdentifierType, _Mapping]] = ..., READ_ONLY: _Optional[_Union[ReadOnlyType, _Mapping]] = ..., FORMAT: _Optional[_Union[FormatType, _Mapping]] = ..., DEPOSIT: _Optional[_Union[DepositType, _Mapping]] = ..., BYTE_ORDER: _Optional[_Union[ByteOrderType, _Mapping]] = ..., FUNCTION_LIST: _Optional[_Union[FunctionListType, _Mapping]] = ..., REF_MEMORY_SEGMENT: _Optional[_Union[RefMemorySegmentType, _Mapping]] = ..., GUARD_RAILS: _Optional[_Union[GuardRailsType, _Mapping]] = ..., EXTENDED_LIMITS: _Optional[_Union[ExtendedLimitsType, _Mapping]] = ..., ANNOTATION: _Optional[_Iterable[_Union[AnnotationType, _Mapping]]] = ..., IF_DATA: _Optional[_Iterable[_Union[_IF_DATA_pb2.IfDataType, _Mapping]]] = ..., CALIBRATION_ACCESS: _Optional[_Union[CalibrationAccessType, _Mapping]] = ..., ECU_ADDRESS_EXTENSION: _Optional[_Union[EcuAddressExtensionType, _Mapping]] = ..., PHYS_UNIT: _Optional[_Union[PhysUnitType, _Mapping]] = ..., STEP_SIZE: _Optional[_Union[StepSizeType, _Mapping]] = ..., SYMBOL_LINK: _Optional[_Union[SymbolLinkType, _Mapping]] = ...) -> None: ...

class AxisPtsXType(_message.Message):
    __slots__ = ("Position", "DataType", "IndexIncr", "Addressing")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    INDEXINCR_FIELD_NUMBER: _ClassVar[int]
    ADDRESSING_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    IndexIncr: IndexOrderType
    Addressing: AddrTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ..., IndexIncr: _Optional[_Union[IndexOrderType, _Mapping]] = ..., Addressing: _Optional[_Union[AddrTypeType, _Mapping]] = ...) -> None: ...

class AxisPtsYType(_message.Message):
    __slots__ = ("Position", "DataType", "IndexIncr", "Addressing")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    INDEXINCR_FIELD_NUMBER: _ClassVar[int]
    ADDRESSING_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    IndexIncr: IndexOrderType
    Addressing: AddrTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ..., IndexIncr: _Optional[_Union[IndexOrderType, _Mapping]] = ..., Addressing: _Optional[_Union[AddrTypeType, _Mapping]] = ...) -> None: ...

class AxisPtsZType(_message.Message):
    __slots__ = ("Position", "DataType", "IndexIncr", "Addressing")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    INDEXINCR_FIELD_NUMBER: _ClassVar[int]
    ADDRESSING_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    IndexIncr: IndexOrderType
    Addressing: AddrTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ..., IndexIncr: _Optional[_Union[IndexOrderType, _Mapping]] = ..., Addressing: _Optional[_Union[AddrTypeType, _Mapping]] = ...) -> None: ...

class AxisRescaleXType(_message.Message):
    __slots__ = ("Position", "DataType", "MaxNumberOfRescalePairs", "IndexIncr", "Addressing")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    MAXNUMBEROFRESCALEPAIRS_FIELD_NUMBER: _ClassVar[int]
    INDEXINCR_FIELD_NUMBER: _ClassVar[int]
    ADDRESSING_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    MaxNumberOfRescalePairs: _shared_pb2.IntType
    IndexIncr: IndexOrderType
    Addressing: AddrTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ..., MaxNumberOfRescalePairs: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., IndexIncr: _Optional[_Union[IndexOrderType, _Mapping]] = ..., Addressing: _Optional[_Union[AddrTypeType, _Mapping]] = ...) -> None: ...

class AxisRescaleYType(_message.Message):
    __slots__ = ("Position", "DataType", "MaxNumberOfRescalePairs", "IndexIncr", "Addressing")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    MAXNUMBEROFRESCALEPAIRS_FIELD_NUMBER: _ClassVar[int]
    INDEXINCR_FIELD_NUMBER: _ClassVar[int]
    ADDRESSING_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    MaxNumberOfRescalePairs: _shared_pb2.IntType
    IndexIncr: IndexOrderType
    Addressing: AddrTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ..., MaxNumberOfRescalePairs: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., IndexIncr: _Optional[_Union[IndexOrderType, _Mapping]] = ..., Addressing: _Optional[_Union[AddrTypeType, _Mapping]] = ...) -> None: ...

class AxisRescaleZType(_message.Message):
    __slots__ = ("Position", "DataType", "MaxNumberOfRescalePairs", "IndexIncr", "Addressing")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    MAXNUMBEROFRESCALEPAIRS_FIELD_NUMBER: _ClassVar[int]
    INDEXINCR_FIELD_NUMBER: _ClassVar[int]
    ADDRESSING_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    MaxNumberOfRescalePairs: _shared_pb2.IntType
    IndexIncr: IndexOrderType
    Addressing: AddrTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ..., MaxNumberOfRescalePairs: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., IndexIncr: _Optional[_Union[IndexOrderType, _Mapping]] = ..., Addressing: _Optional[_Union[AddrTypeType, _Mapping]] = ...) -> None: ...

class BitOperationType(_message.Message):
    __slots__ = ("LEFT_SHIFT", "RIGHT_SHIFT", "SIGN_EXTEND")
    LEFT_SHIFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_SHIFT_FIELD_NUMBER: _ClassVar[int]
    SIGN_EXTEND_FIELD_NUMBER: _ClassVar[int]
    LEFT_SHIFT: LeftShiftType
    RIGHT_SHIFT: RightShiftType
    SIGN_EXTEND: SignExtendType
    def __init__(self, LEFT_SHIFT: _Optional[_Union[LeftShiftType, _Mapping]] = ..., RIGHT_SHIFT: _Optional[_Union[RightShiftType, _Mapping]] = ..., SIGN_EXTEND: _Optional[_Union[SignExtendType, _Mapping]] = ...) -> None: ...

class BitMaskType(_message.Message):
    __slots__ = ("Mask",)
    MASK_FIELD_NUMBER: _ClassVar[int]
    Mask: _shared_pb2.LongType
    def __init__(self, Mask: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ...) -> None: ...

class ByteOrderType(_message.Message):
    __slots__ = ("ByteOrder",)
    BYTEORDER_FIELD_NUMBER: _ClassVar[int]
    ByteOrder: str
    def __init__(self, ByteOrder: _Optional[str] = ...) -> None: ...

class CalibrationAccessType(_message.Message):
    __slots__ = ("Type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    Type: str
    def __init__(self, Type: _Optional[str] = ...) -> None: ...

class CalibrationHandleType(_message.Message):
    __slots__ = ("Handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    Handle: _containers.RepeatedCompositeFieldContainer[_shared_pb2.LongType]
    def __init__(self, Handle: _Optional[_Iterable[_Union[_shared_pb2.LongType, _Mapping]]] = ...) -> None: ...

class CalibrationMethodType(_message.Message):
    __slots__ = ("Method", "Version", "CALIBRATION_HANDLE")
    METHOD_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CALIBRATION_HANDLE_FIELD_NUMBER: _ClassVar[int]
    Method: _shared_pb2.StringType
    Version: _shared_pb2.LongType
    CALIBRATION_HANDLE: _containers.RepeatedCompositeFieldContainer[CalibrationHandleType]
    def __init__(self, Method: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Version: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ..., CALIBRATION_HANDLE: _Optional[_Iterable[_Union[CalibrationHandleType, _Mapping]]] = ...) -> None: ...

class CharacteristicType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "Type", "Address", "Deposit", "MaxDiff", "Conversion", "LowerLimit", "UpperLimit", "DISPLAY_IDENTIFIER", "FORMAT", "BYTE_ORDER", "BIT_MASK", "FUNCTION_LIST", "NUMBER", "EXTENDED_LIMITS", "READ_ONLY", "GUARD_RAILS", "MAP_LIST", "MAX_REFRESH", "DEPENDENT_CHARACTERISTIC", "VIRTUAL_CHARACTERISTIC", "REF_MEMORY_SEGMENT", "ANNOTATION", "COMPARISON_QUANTITY", "IF_DATA", "AXIS_DESCR", "CALIBRATION_ACCESS", "MATRIX_DIM", "ECU_ADDRESS_EXTENSION", "DISCRETE", "SYMBOL_LINK", "STEP_SIZE", "PHYS_UNIT")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    MAXDIFF_FIELD_NUMBER: _ClassVar[int]
    CONVERSION_FIELD_NUMBER: _ClassVar[int]
    LOWERLIMIT_FIELD_NUMBER: _ClassVar[int]
    UPPERLIMIT_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    BYTE_ORDER_FIELD_NUMBER: _ClassVar[int]
    BIT_MASK_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_LIST_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_LIMITS_FIELD_NUMBER: _ClassVar[int]
    READ_ONLY_FIELD_NUMBER: _ClassVar[int]
    GUARD_RAILS_FIELD_NUMBER: _ClassVar[int]
    MAP_LIST_FIELD_NUMBER: _ClassVar[int]
    MAX_REFRESH_FIELD_NUMBER: _ClassVar[int]
    DEPENDENT_CHARACTERISTIC_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_CHARACTERISTIC_FIELD_NUMBER: _ClassVar[int]
    REF_MEMORY_SEGMENT_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_FIELD_NUMBER: _ClassVar[int]
    COMPARISON_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    IF_DATA_FIELD_NUMBER: _ClassVar[int]
    AXIS_DESCR_FIELD_NUMBER: _ClassVar[int]
    CALIBRATION_ACCESS_FIELD_NUMBER: _ClassVar[int]
    MATRIX_DIM_FIELD_NUMBER: _ClassVar[int]
    ECU_ADDRESS_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    DISCRETE_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_LINK_FIELD_NUMBER: _ClassVar[int]
    STEP_SIZE_FIELD_NUMBER: _ClassVar[int]
    PHYS_UNIT_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    Type: str
    Address: _shared_pb2.LongType
    Deposit: _shared_pb2.IdentType
    MaxDiff: _shared_pb2.FloatType
    Conversion: _shared_pb2.IdentType
    LowerLimit: _shared_pb2.FloatType
    UpperLimit: _shared_pb2.FloatType
    DISPLAY_IDENTIFIER: DisplayIdentifierType
    FORMAT: FormatType
    BYTE_ORDER: ByteOrderType
    BIT_MASK: BitMaskType
    FUNCTION_LIST: FunctionListType
    NUMBER: NumberType
    EXTENDED_LIMITS: ExtendedLimitsType
    READ_ONLY: ReadOnlyType
    GUARD_RAILS: GuardRailsType
    MAP_LIST: MapListType
    MAX_REFRESH: MaxRefreshType
    DEPENDENT_CHARACTERISTIC: DependentCharacteristicType
    VIRTUAL_CHARACTERISTIC: VirtualCharacteristicType
    REF_MEMORY_SEGMENT: RefMemorySegmentType
    ANNOTATION: _containers.RepeatedCompositeFieldContainer[AnnotationType]
    COMPARISON_QUANTITY: ComparisonQuantityType
    IF_DATA: _containers.RepeatedCompositeFieldContainer[_IF_DATA_pb2.IfDataType]
    AXIS_DESCR: _containers.RepeatedCompositeFieldContainer[AxisDescrType]
    CALIBRATION_ACCESS: CalibrationAccessType
    MATRIX_DIM: MatrixDimType
    ECU_ADDRESS_EXTENSION: EcuAddressExtensionType
    DISCRETE: DiscreteType
    SYMBOL_LINK: SymbolLinkType
    STEP_SIZE: StepSizeType
    PHYS_UNIT: PhysUnitType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Type: _Optional[str] = ..., Address: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ..., Deposit: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., MaxDiff: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., Conversion: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LowerLimit: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., UpperLimit: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., DISPLAY_IDENTIFIER: _Optional[_Union[DisplayIdentifierType, _Mapping]] = ..., FORMAT: _Optional[_Union[FormatType, _Mapping]] = ..., BYTE_ORDER: _Optional[_Union[ByteOrderType, _Mapping]] = ..., BIT_MASK: _Optional[_Union[BitMaskType, _Mapping]] = ..., FUNCTION_LIST: _Optional[_Union[FunctionListType, _Mapping]] = ..., NUMBER: _Optional[_Union[NumberType, _Mapping]] = ..., EXTENDED_LIMITS: _Optional[_Union[ExtendedLimitsType, _Mapping]] = ..., READ_ONLY: _Optional[_Union[ReadOnlyType, _Mapping]] = ..., GUARD_RAILS: _Optional[_Union[GuardRailsType, _Mapping]] = ..., MAP_LIST: _Optional[_Union[MapListType, _Mapping]] = ..., MAX_REFRESH: _Optional[_Union[MaxRefreshType, _Mapping]] = ..., DEPENDENT_CHARACTERISTIC: _Optional[_Union[DependentCharacteristicType, _Mapping]] = ..., VIRTUAL_CHARACTERISTIC: _Optional[_Union[VirtualCharacteristicType, _Mapping]] = ..., REF_MEMORY_SEGMENT: _Optional[_Union[RefMemorySegmentType, _Mapping]] = ..., ANNOTATION: _Optional[_Iterable[_Union[AnnotationType, _Mapping]]] = ..., COMPARISON_QUANTITY: _Optional[_Union[ComparisonQuantityType, _Mapping]] = ..., IF_DATA: _Optional[_Iterable[_Union[_IF_DATA_pb2.IfDataType, _Mapping]]] = ..., AXIS_DESCR: _Optional[_Iterable[_Union[AxisDescrType, _Mapping]]] = ..., CALIBRATION_ACCESS: _Optional[_Union[CalibrationAccessType, _Mapping]] = ..., MATRIX_DIM: _Optional[_Union[MatrixDimType, _Mapping]] = ..., ECU_ADDRESS_EXTENSION: _Optional[_Union[EcuAddressExtensionType, _Mapping]] = ..., DISCRETE: _Optional[_Union[DiscreteType, _Mapping]] = ..., SYMBOL_LINK: _Optional[_Union[SymbolLinkType, _Mapping]] = ..., STEP_SIZE: _Optional[_Union[StepSizeType, _Mapping]] = ..., PHYS_UNIT: _Optional[_Union[PhysUnitType, _Mapping]] = ...) -> None: ...

class CoeffsType(_message.Message):
    __slots__ = ("A", "B", "C", "D", "E", "F")
    A_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    C_FIELD_NUMBER: _ClassVar[int]
    D_FIELD_NUMBER: _ClassVar[int]
    E_FIELD_NUMBER: _ClassVar[int]
    F_FIELD_NUMBER: _ClassVar[int]
    A: _shared_pb2.FloatType
    B: _shared_pb2.FloatType
    C: _shared_pb2.FloatType
    D: _shared_pb2.FloatType
    E: _shared_pb2.FloatType
    F: _shared_pb2.FloatType
    def __init__(self, A: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., B: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., C: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., D: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., E: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., F: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ...) -> None: ...

class CoeffsLinearType(_message.Message):
    __slots__ = ("A", "B")
    A_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    A: _shared_pb2.FloatType
    B: _shared_pb2.FloatType
    def __init__(self, A: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., B: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ...) -> None: ...

class ComparisonQuantityType(_message.Message):
    __slots__ = ("Name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class CompuMethodType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "ConversionType", "Format", "Unit", "FORMULA", "COEFFS", "COEFFS_LINEAR", "COMPU_TAB_REF", "REF_UNIT")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CONVERSIONTYPE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    FORMULA_FIELD_NUMBER: _ClassVar[int]
    COEFFS_FIELD_NUMBER: _ClassVar[int]
    COEFFS_LINEAR_FIELD_NUMBER: _ClassVar[int]
    COMPU_TAB_REF_FIELD_NUMBER: _ClassVar[int]
    REF_UNIT_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    ConversionType: str
    Format: _shared_pb2.StringType
    Unit: _shared_pb2.StringType
    FORMULA: FormulaType
    COEFFS: CoeffsType
    COEFFS_LINEAR: CoeffsLinearType
    COMPU_TAB_REF: CompuTabRefType
    REF_UNIT: RefUnitType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., ConversionType: _Optional[str] = ..., Format: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Unit: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., FORMULA: _Optional[_Union[FormulaType, _Mapping]] = ..., COEFFS: _Optional[_Union[CoeffsType, _Mapping]] = ..., COEFFS_LINEAR: _Optional[_Union[CoeffsLinearType, _Mapping]] = ..., COMPU_TAB_REF: _Optional[_Union[CompuTabRefType, _Mapping]] = ..., REF_UNIT: _Optional[_Union[RefUnitType, _Mapping]] = ...) -> None: ...

class CompuTabRefType(_message.Message):
    __slots__ = ("ConversionTable",)
    CONVERSIONTABLE_FIELD_NUMBER: _ClassVar[int]
    ConversionTable: _shared_pb2.IdentType
    def __init__(self, ConversionTable: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class CompuTabType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "ConversionType", "NumberValuePairs", "InValOutVal", "DEFAULT_VALUE")
    class InValOutValType(_message.Message):
        __slots__ = ("InVal", "OutVal")
        INVAL_FIELD_NUMBER: _ClassVar[int]
        OUTVAL_FIELD_NUMBER: _ClassVar[int]
        InVal: _shared_pb2.FloatType
        OutVal: _shared_pb2.FloatType
        def __init__(self, InVal: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., OutVal: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CONVERSIONTYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBERVALUEPAIRS_FIELD_NUMBER: _ClassVar[int]
    INVALOUTVAL_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    ConversionType: str
    NumberValuePairs: _shared_pb2.IntType
    InValOutVal: _containers.RepeatedCompositeFieldContainer[CompuTabType.InValOutValType]
    DEFAULT_VALUE: DefaultValueType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., ConversionType: _Optional[str] = ..., NumberValuePairs: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., InValOutVal: _Optional[_Iterable[_Union[CompuTabType.InValOutValType, _Mapping]]] = ..., DEFAULT_VALUE: _Optional[_Union[DefaultValueType, _Mapping]] = ...) -> None: ...

class CompuVTabRangeType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "NumberOfValuesTriples", "InValMinInValMaxOutVal", "DEFAULT_VALUE")
    class InValMinInValMaxOutValType(_message.Message):
        __slots__ = ("InValMin", "InValMax", "OutVal")
        INVALMIN_FIELD_NUMBER: _ClassVar[int]
        INVALMAX_FIELD_NUMBER: _ClassVar[int]
        OUTVAL_FIELD_NUMBER: _ClassVar[int]
        InValMin: _shared_pb2.FloatType
        InValMax: _shared_pb2.FloatType
        OutVal: _shared_pb2.StringType
        def __init__(self, InValMin: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., InValMax: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., OutVal: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    NUMBEROFVALUESTRIPLES_FIELD_NUMBER: _ClassVar[int]
    INVALMININVALMAXOUTVAL_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    NumberOfValuesTriples: _shared_pb2.IntType
    InValMinInValMaxOutVal: _containers.RepeatedCompositeFieldContainer[CompuVTabRangeType.InValMinInValMaxOutValType]
    DEFAULT_VALUE: DefaultValueType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., NumberOfValuesTriples: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., InValMinInValMaxOutVal: _Optional[_Iterable[_Union[CompuVTabRangeType.InValMinInValMaxOutValType, _Mapping]]] = ..., DEFAULT_VALUE: _Optional[_Union[DefaultValueType, _Mapping]] = ...) -> None: ...

class CompuVTabType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "ConversionType", "NumberValuePairs", "InValOutVal", "DEFAULT_VALUE")
    class InValOutValType(_message.Message):
        __slots__ = ("InVal", "OutVal")
        INVAL_FIELD_NUMBER: _ClassVar[int]
        OUTVAL_FIELD_NUMBER: _ClassVar[int]
        InVal: _shared_pb2.FloatType
        OutVal: _shared_pb2.StringType
        def __init__(self, InVal: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., OutVal: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CONVERSIONTYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBERVALUEPAIRS_FIELD_NUMBER: _ClassVar[int]
    INVALOUTVAL_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    ConversionType: str
    NumberValuePairs: _shared_pb2.IntType
    InValOutVal: _containers.RepeatedCompositeFieldContainer[CompuVTabType.InValOutValType]
    DEFAULT_VALUE: DefaultValueType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., ConversionType: _Optional[str] = ..., NumberValuePairs: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., InValOutVal: _Optional[_Iterable[_Union[CompuVTabType.InValOutValType, _Mapping]]] = ..., DEFAULT_VALUE: _Optional[_Union[DefaultValueType, _Mapping]] = ...) -> None: ...

class CpuTypeType(_message.Message):
    __slots__ = ("Cpu",)
    CPU_FIELD_NUMBER: _ClassVar[int]
    Cpu: _shared_pb2.StringType
    def __init__(self, Cpu: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class CurveAxisRefType(_message.Message):
    __slots__ = ("CurveAxis",)
    CURVEAXIS_FIELD_NUMBER: _ClassVar[int]
    CurveAxis: _shared_pb2.IdentType
    def __init__(self, CurveAxis: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class CustomerNoType(_message.Message):
    __slots__ = ("Number",)
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    Number: _shared_pb2.StringType
    def __init__(self, Number: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class CustomerType(_message.Message):
    __slots__ = ("Customer",)
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    Customer: _shared_pb2.StringType
    def __init__(self, Customer: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class DataSizeType(_message.Message):
    __slots__ = ("Size",)
    SIZE_FIELD_NUMBER: _ClassVar[int]
    Size: _shared_pb2.IntType
    def __init__(self, Size: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class DefaultValueType(_message.Message):
    __slots__ = ("DisplayString",)
    DISPLAYSTRING_FIELD_NUMBER: _ClassVar[int]
    DisplayString: _shared_pb2.StringType
    def __init__(self, DisplayString: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class DefCharacteristicType(_message.Message):
    __slots__ = ("Identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Identifier: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Identifier: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class DependentCharacteristicType(_message.Message):
    __slots__ = ("Formula", "Characteristic")
    FORMULA_FIELD_NUMBER: _ClassVar[int]
    CHARACTERISTIC_FIELD_NUMBER: _ClassVar[int]
    Formula: _shared_pb2.StringType
    Characteristic: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Formula: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Characteristic: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class DepositType(_message.Message):
    __slots__ = ("Mode",)
    MODE_FIELD_NUMBER: _ClassVar[int]
    Mode: str
    def __init__(self, Mode: _Optional[str] = ...) -> None: ...

class DiscreteType(_message.Message):
    __slots__ = ("Present",)
    PRESENT_FIELD_NUMBER: _ClassVar[int]
    Present: bool
    def __init__(self, Present: bool = ...) -> None: ...

class DisplayIdentifierType(_message.Message):
    __slots__ = ("DisplayName",)
    DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    DisplayName: _shared_pb2.IdentType
    def __init__(self, DisplayName: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class DistOpXType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class DistOpYType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class DistOpZType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class EcuAddressExtensionType(_message.Message):
    __slots__ = ("Extension",)
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    Extension: _shared_pb2.IntType
    def __init__(self, Extension: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class EcuAddressType(_message.Message):
    __slots__ = ("Address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    Address: _shared_pb2.LongType
    def __init__(self, Address: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ...) -> None: ...

class EcuCalibrationOffsetType(_message.Message):
    __slots__ = ("Offset",)
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    Offset: _shared_pb2.LongType
    def __init__(self, Offset: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ...) -> None: ...

class EcuType(_message.Message):
    __slots__ = ("ControlUnit",)
    CONTROLUNIT_FIELD_NUMBER: _ClassVar[int]
    ControlUnit: _shared_pb2.StringType
    def __init__(self, ControlUnit: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class EpkType(_message.Message):
    __slots__ = ("Identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Identifier: _shared_pb2.StringType
    def __init__(self, Identifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class ErrorMaskType(_message.Message):
    __slots__ = ("Mask",)
    MASK_FIELD_NUMBER: _ClassVar[int]
    Mask: _shared_pb2.LongType
    def __init__(self, Mask: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ...) -> None: ...

class ExtendedLimitsType(_message.Message):
    __slots__ = ("LowerLimit", "UpperLimit")
    LOWERLIMIT_FIELD_NUMBER: _ClassVar[int]
    UPPERLIMIT_FIELD_NUMBER: _ClassVar[int]
    LowerLimit: _shared_pb2.FloatType
    UpperLimit: _shared_pb2.FloatType
    def __init__(self, LowerLimit: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., UpperLimit: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ...) -> None: ...

class FixAxisParDistType(_message.Message):
    __slots__ = ("Offset", "Distance", "Numberapo")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    NUMBERAPO_FIELD_NUMBER: _ClassVar[int]
    Offset: _shared_pb2.IntType
    Distance: _shared_pb2.IntType
    Numberapo: _shared_pb2.IntType
    def __init__(self, Offset: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., Distance: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., Numberapo: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class FixAxisParListType(_message.Message):
    __slots__ = ("AxisPtsValue",)
    AXISPTSVALUE_FIELD_NUMBER: _ClassVar[int]
    AxisPtsValue: _containers.RepeatedCompositeFieldContainer[_shared_pb2.FloatType]
    def __init__(self, AxisPtsValue: _Optional[_Iterable[_Union[_shared_pb2.FloatType, _Mapping]]] = ...) -> None: ...

class FixAxisParType(_message.Message):
    __slots__ = ("Offset", "Shift", "Numberapo")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    SHIFT_FIELD_NUMBER: _ClassVar[int]
    NUMBERAPO_FIELD_NUMBER: _ClassVar[int]
    Offset: _shared_pb2.IntType
    Shift: _shared_pb2.IntType
    Numberapo: _shared_pb2.IntType
    def __init__(self, Offset: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., Shift: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., Numberapo: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class FixNoAxisPtsXType(_message.Message):
    __slots__ = ("NumberOfAxisPoints",)
    NUMBEROFAXISPOINTS_FIELD_NUMBER: _ClassVar[int]
    NumberOfAxisPoints: _shared_pb2.IntType
    def __init__(self, NumberOfAxisPoints: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class FixNoAxisPtsYType(_message.Message):
    __slots__ = ("NumberOfAxisPoints",)
    NUMBEROFAXISPOINTS_FIELD_NUMBER: _ClassVar[int]
    NumberOfAxisPoints: _shared_pb2.IntType
    def __init__(self, NumberOfAxisPoints: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class FixNoAxisPtsZType(_message.Message):
    __slots__ = ("NumberOfAxisPoints",)
    NUMBEROFAXISPOINTS_FIELD_NUMBER: _ClassVar[int]
    NumberOfAxisPoints: _shared_pb2.IntType
    def __init__(self, NumberOfAxisPoints: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class FncValuesType(_message.Message):
    __slots__ = ("Position", "DataType", "IndexMode", "AddressType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    INDEXMODE_FIELD_NUMBER: _ClassVar[int]
    ADDRESSTYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    IndexMode: str
    AddressType: AddrTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ..., IndexMode: _Optional[str] = ..., AddressType: _Optional[_Union[AddrTypeType, _Mapping]] = ...) -> None: ...

class FormatType(_message.Message):
    __slots__ = ("FormatString",)
    FORMATSTRING_FIELD_NUMBER: _ClassVar[int]
    FormatString: _shared_pb2.StringType
    def __init__(self, FormatString: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class FormulaInvType(_message.Message):
    __slots__ = ("GX",)
    GX_FIELD_NUMBER: _ClassVar[int]
    GX: _shared_pb2.StringType
    def __init__(self, GX: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class FormulaType(_message.Message):
    __slots__ = ("FX", "FORMULA_INV")
    FX_FIELD_NUMBER: _ClassVar[int]
    FORMULA_INV_FIELD_NUMBER: _ClassVar[int]
    FX: _shared_pb2.StringType
    FORMULA_INV: FormulaInvType
    def __init__(self, FX: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., FORMULA_INV: _Optional[_Union[FormulaInvType, _Mapping]] = ...) -> None: ...

class FrameMeasurementType(_message.Message):
    __slots__ = ("Identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Identifier: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Identifier: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class FrameType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "ScalingUnit", "Rate", "FRAME_MEASUREMENT", "IF_DATA")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    SCALINGUNIT_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    FRAME_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    IF_DATA_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    ScalingUnit: _shared_pb2.IntType
    Rate: _shared_pb2.LongType
    FRAME_MEASUREMENT: FrameMeasurementType
    IF_DATA: _containers.RepeatedCompositeFieldContainer[_IF_DATA_pb2.IfDataType]
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., ScalingUnit: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., Rate: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ..., FRAME_MEASUREMENT: _Optional[_Union[FrameMeasurementType, _Mapping]] = ..., IF_DATA: _Optional[_Iterable[_Union[_IF_DATA_pb2.IfDataType, _Mapping]]] = ...) -> None: ...

class FunctionListType(_message.Message):
    __slots__ = ("Name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    Name: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Name: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class FunctionType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "ANNOTATION", "DEF_CHARACTERISTIC", "REF_CHARACTERISTIC", "IN_MEASUREMENT", "OUT_MEASUREMENT", "LOC_MEASUREMENT", "SUB_FUNCTION", "FUNCTION_VERSION")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_FIELD_NUMBER: _ClassVar[int]
    DEF_CHARACTERISTIC_FIELD_NUMBER: _ClassVar[int]
    REF_CHARACTERISTIC_FIELD_NUMBER: _ClassVar[int]
    IN_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    OUT_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    LOC_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    SUB_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_VERSION_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    ANNOTATION: _containers.RepeatedCompositeFieldContainer[AnnotationType]
    DEF_CHARACTERISTIC: DefCharacteristicType
    REF_CHARACTERISTIC: RefCharacteristicType
    IN_MEASUREMENT: InMeasurementType
    OUT_MEASUREMENT: OutMeasurementType
    LOC_MEASUREMENT: LocMeasurementType
    SUB_FUNCTION: SubFunctionType
    FUNCTION_VERSION: FunctionVersionType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., ANNOTATION: _Optional[_Iterable[_Union[AnnotationType, _Mapping]]] = ..., DEF_CHARACTERISTIC: _Optional[_Union[DefCharacteristicType, _Mapping]] = ..., REF_CHARACTERISTIC: _Optional[_Union[RefCharacteristicType, _Mapping]] = ..., IN_MEASUREMENT: _Optional[_Union[InMeasurementType, _Mapping]] = ..., OUT_MEASUREMENT: _Optional[_Union[OutMeasurementType, _Mapping]] = ..., LOC_MEASUREMENT: _Optional[_Union[LocMeasurementType, _Mapping]] = ..., SUB_FUNCTION: _Optional[_Union[SubFunctionType, _Mapping]] = ..., FUNCTION_VERSION: _Optional[_Union[FunctionVersionType, _Mapping]] = ...) -> None: ...

class FunctionVersionType(_message.Message):
    __slots__ = ("VersionIdentifier",)
    VERSIONIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    VersionIdentifier: _shared_pb2.StringType
    def __init__(self, VersionIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class GroupType(_message.Message):
    __slots__ = ("GroupName", "GroupLongIdentifier", "ANNOTATION", "ROOT", "REF_CHARACTERISTIC", "REF_MEASUREMENT", "FUNCTION_LIST", "SUB_GROUP")
    GROUPNAME_FIELD_NUMBER: _ClassVar[int]
    GROUPLONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_FIELD_NUMBER: _ClassVar[int]
    ROOT_FIELD_NUMBER: _ClassVar[int]
    REF_CHARACTERISTIC_FIELD_NUMBER: _ClassVar[int]
    REF_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_LIST_FIELD_NUMBER: _ClassVar[int]
    SUB_GROUP_FIELD_NUMBER: _ClassVar[int]
    GroupName: _shared_pb2.IdentType
    GroupLongIdentifier: _shared_pb2.StringType
    ANNOTATION: _containers.RepeatedCompositeFieldContainer[AnnotationType]
    ROOT: RootType
    REF_CHARACTERISTIC: RefCharacteristicType
    REF_MEASUREMENT: RefMeasurementType
    FUNCTION_LIST: FunctionListType
    SUB_GROUP: SubGroupType
    def __init__(self, GroupName: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., GroupLongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., ANNOTATION: _Optional[_Iterable[_Union[AnnotationType, _Mapping]]] = ..., ROOT: _Optional[_Union[RootType, _Mapping]] = ..., REF_CHARACTERISTIC: _Optional[_Union[RefCharacteristicType, _Mapping]] = ..., REF_MEASUREMENT: _Optional[_Union[RefMeasurementType, _Mapping]] = ..., FUNCTION_LIST: _Optional[_Union[FunctionListType, _Mapping]] = ..., SUB_GROUP: _Optional[_Union[SubGroupType, _Mapping]] = ...) -> None: ...

class GuardRailsType(_message.Message):
    __slots__ = ("Present",)
    PRESENT_FIELD_NUMBER: _ClassVar[int]
    Present: bool
    def __init__(self, Present: bool = ...) -> None: ...

class HeaderType(_message.Message):
    __slots__ = ("Comment", "VERSION", "PROJECT_NO")
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NO_FIELD_NUMBER: _ClassVar[int]
    Comment: _shared_pb2.StringType
    VERSION: VersionType
    PROJECT_NO: ProjectNoType
    def __init__(self, Comment: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., VERSION: _Optional[_Union[VersionType, _Mapping]] = ..., PROJECT_NO: _Optional[_Union[ProjectNoType, _Mapping]] = ...) -> None: ...

class IdentificationType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class InMeasurementType(_message.Message):
    __slots__ = ("Identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Identifier: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Identifier: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class LayoutType(_message.Message):
    __slots__ = ("IndexMode",)
    INDEXMODE_FIELD_NUMBER: _ClassVar[int]
    IndexMode: str
    def __init__(self, IndexMode: _Optional[str] = ...) -> None: ...

class LeftShiftType(_message.Message):
    __slots__ = ("BitCount",)
    BITCOUNT_FIELD_NUMBER: _ClassVar[int]
    BitCount: _shared_pb2.LongType
    def __init__(self, BitCount: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ...) -> None: ...

class LocMeasurementType(_message.Message):
    __slots__ = ("Identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Identifier: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Identifier: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class MapListType(_message.Message):
    __slots__ = ("Name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    Name: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Name: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class MatrixDimType(_message.Message):
    __slots__ = ("XDim", "YDim", "ZDim")
    XDIM_FIELD_NUMBER: _ClassVar[int]
    YDIM_FIELD_NUMBER: _ClassVar[int]
    ZDIM_FIELD_NUMBER: _ClassVar[int]
    XDim: _shared_pb2.IntType
    YDim: _shared_pb2.IntType
    ZDim: _shared_pb2.IntType
    def __init__(self, XDim: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., YDim: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., ZDim: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class MaxGradType(_message.Message):
    __slots__ = ("MaxGradient",)
    MAXGRADIENT_FIELD_NUMBER: _ClassVar[int]
    MaxGradient: _shared_pb2.FloatType
    def __init__(self, MaxGradient: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ...) -> None: ...

class MaxRefreshType(_message.Message):
    __slots__ = ("ScalingUnit", "Rate")
    SCALINGUNIT_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    ScalingUnit: _shared_pb2.IntType
    Rate: _shared_pb2.LongType
    def __init__(self, ScalingUnit: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., Rate: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ...) -> None: ...

class MeasurementType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "DataType", "Conversion", "Resolution", "Accuracy", "LowerLimit", "UpperLimit", "DISPLAY_IDENTIFIER", "READ_WRITE", "FORMAT", "ARRAY_SIZE", "BIT_MASK", "BIT_OPERATION", "BYTE_ORDER", "MAX_REFRESH", "VIRTUAL", "FUNCTION_LIST", "ECU_ADDRESS", "ERROR_MASK", "REF_MEMORY_SEGMENT", "ANNOTATION", "IF_DATA", "MATRIX_DIM", "ECU_ADDRESS_EXTENSION", "DISCRETE", "SYMBOL_LINK", "LAYOUT", "PHYS_UNIT")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    CONVERSION_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    LOWERLIMIT_FIELD_NUMBER: _ClassVar[int]
    UPPERLIMIT_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    READ_WRITE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    ARRAY_SIZE_FIELD_NUMBER: _ClassVar[int]
    BIT_MASK_FIELD_NUMBER: _ClassVar[int]
    BIT_OPERATION_FIELD_NUMBER: _ClassVar[int]
    BYTE_ORDER_FIELD_NUMBER: _ClassVar[int]
    MAX_REFRESH_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_LIST_FIELD_NUMBER: _ClassVar[int]
    ECU_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MASK_FIELD_NUMBER: _ClassVar[int]
    REF_MEMORY_SEGMENT_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_FIELD_NUMBER: _ClassVar[int]
    IF_DATA_FIELD_NUMBER: _ClassVar[int]
    MATRIX_DIM_FIELD_NUMBER: _ClassVar[int]
    ECU_ADDRESS_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    DISCRETE_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_LINK_FIELD_NUMBER: _ClassVar[int]
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    PHYS_UNIT_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    DataType: DataTypeType
    Conversion: _shared_pb2.IdentType
    Resolution: _shared_pb2.IntType
    Accuracy: _shared_pb2.FloatType
    LowerLimit: _shared_pb2.FloatType
    UpperLimit: _shared_pb2.FloatType
    DISPLAY_IDENTIFIER: DisplayIdentifierType
    READ_WRITE: ReadWriteType
    FORMAT: FormatType
    ARRAY_SIZE: ArraySizeType
    BIT_MASK: BitMaskType
    BIT_OPERATION: BitOperationType
    BYTE_ORDER: ByteOrderType
    MAX_REFRESH: MaxRefreshType
    VIRTUAL: VirtualType
    FUNCTION_LIST: FunctionListType
    ECU_ADDRESS: EcuAddressType
    ERROR_MASK: ErrorMaskType
    REF_MEMORY_SEGMENT: RefMemorySegmentType
    ANNOTATION: _containers.RepeatedCompositeFieldContainer[AnnotationType]
    IF_DATA: _containers.RepeatedCompositeFieldContainer[_IF_DATA_pb2.IfDataType]
    MATRIX_DIM: MatrixDimType
    ECU_ADDRESS_EXTENSION: EcuAddressExtensionType
    DISCRETE: DiscreteType
    SYMBOL_LINK: SymbolLinkType
    LAYOUT: LayoutType
    PHYS_UNIT: PhysUnitType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ..., Conversion: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., Resolution: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., Accuracy: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., LowerLimit: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., UpperLimit: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., DISPLAY_IDENTIFIER: _Optional[_Union[DisplayIdentifierType, _Mapping]] = ..., READ_WRITE: _Optional[_Union[ReadWriteType, _Mapping]] = ..., FORMAT: _Optional[_Union[FormatType, _Mapping]] = ..., ARRAY_SIZE: _Optional[_Union[ArraySizeType, _Mapping]] = ..., BIT_MASK: _Optional[_Union[BitMaskType, _Mapping]] = ..., BIT_OPERATION: _Optional[_Union[BitOperationType, _Mapping]] = ..., BYTE_ORDER: _Optional[_Union[ByteOrderType, _Mapping]] = ..., MAX_REFRESH: _Optional[_Union[MaxRefreshType, _Mapping]] = ..., VIRTUAL: _Optional[_Union[VirtualType, _Mapping]] = ..., FUNCTION_LIST: _Optional[_Union[FunctionListType, _Mapping]] = ..., ECU_ADDRESS: _Optional[_Union[EcuAddressType, _Mapping]] = ..., ERROR_MASK: _Optional[_Union[ErrorMaskType, _Mapping]] = ..., REF_MEMORY_SEGMENT: _Optional[_Union[RefMemorySegmentType, _Mapping]] = ..., ANNOTATION: _Optional[_Iterable[_Union[AnnotationType, _Mapping]]] = ..., IF_DATA: _Optional[_Iterable[_Union[_IF_DATA_pb2.IfDataType, _Mapping]]] = ..., MATRIX_DIM: _Optional[_Union[MatrixDimType, _Mapping]] = ..., ECU_ADDRESS_EXTENSION: _Optional[_Union[EcuAddressExtensionType, _Mapping]] = ..., DISCRETE: _Optional[_Union[DiscreteType, _Mapping]] = ..., SYMBOL_LINK: _Optional[_Union[SymbolLinkType, _Mapping]] = ..., LAYOUT: _Optional[_Union[LayoutType, _Mapping]] = ..., PHYS_UNIT: _Optional[_Union[PhysUnitType, _Mapping]] = ...) -> None: ...

class MemoryLayoutType(_message.Message):
    __slots__ = ("PrgType", "Address", "Size", "Offset", "IF_DATA")
    PRGTYPE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    IF_DATA_FIELD_NUMBER: _ClassVar[int]
    PrgType: str
    Address: _shared_pb2.LongType
    Size: _shared_pb2.LongType
    Offset: _containers.RepeatedCompositeFieldContainer[_shared_pb2.LongType]
    IF_DATA: _containers.RepeatedCompositeFieldContainer[_IF_DATA_pb2.IfDataType]
    def __init__(self, PrgType: _Optional[str] = ..., Address: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ..., Size: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ..., Offset: _Optional[_Iterable[_Union[_shared_pb2.LongType, _Mapping]]] = ..., IF_DATA: _Optional[_Iterable[_Union[_IF_DATA_pb2.IfDataType, _Mapping]]] = ...) -> None: ...

class MemorySegmentType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "PrgType", "MemoryType", "Attribute", "Address", "Size", "Offset", "IF_DATA")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PRGTYPE_FIELD_NUMBER: _ClassVar[int]
    MEMORYTYPE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    IF_DATA_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    PrgType: str
    MemoryType: str
    Attribute: str
    Address: _shared_pb2.LongType
    Size: _shared_pb2.LongType
    Offset: _containers.RepeatedCompositeFieldContainer[_shared_pb2.LongType]
    IF_DATA: _containers.RepeatedCompositeFieldContainer[_IF_DATA_pb2.IfDataType]
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., PrgType: _Optional[str] = ..., MemoryType: _Optional[str] = ..., Attribute: _Optional[str] = ..., Address: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ..., Size: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ..., Offset: _Optional[_Iterable[_Union[_shared_pb2.LongType, _Mapping]]] = ..., IF_DATA: _Optional[_Iterable[_Union[_IF_DATA_pb2.IfDataType, _Mapping]]] = ...) -> None: ...

class ModCommonType(_message.Message):
    __slots__ = ("Comment", "S_REC_LAYOUT", "DEPOSIT", "BYTE_ORDER", "DATA_SIZE", "ALIGNMENT_BYTE", "ALIGNMENT_WORD", "ALIGNMENT_LONG", "ALIGNMENT_FLOAT32_IEEE", "ALIGNMENT_FLOAT64_IEEE")
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    S_REC_LAYOUT_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    BYTE_ORDER_FIELD_NUMBER: _ClassVar[int]
    DATA_SIZE_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_BYTE_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_WORD_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_LONG_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_FLOAT32_IEEE_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_FLOAT64_IEEE_FIELD_NUMBER: _ClassVar[int]
    Comment: _shared_pb2.StringType
    S_REC_LAYOUT: SRecLayoutType
    DEPOSIT: DepositType
    BYTE_ORDER: ByteOrderType
    DATA_SIZE: DataSizeType
    ALIGNMENT_BYTE: AlignmentByteType
    ALIGNMENT_WORD: AlignmentWordType
    ALIGNMENT_LONG: AlignmentLongType
    ALIGNMENT_FLOAT32_IEEE: AlignmentFloat32IeeeType
    ALIGNMENT_FLOAT64_IEEE: AlignmentFloat64IeeeType
    def __init__(self, Comment: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., S_REC_LAYOUT: _Optional[_Union[SRecLayoutType, _Mapping]] = ..., DEPOSIT: _Optional[_Union[DepositType, _Mapping]] = ..., BYTE_ORDER: _Optional[_Union[ByteOrderType, _Mapping]] = ..., DATA_SIZE: _Optional[_Union[DataSizeType, _Mapping]] = ..., ALIGNMENT_BYTE: _Optional[_Union[AlignmentByteType, _Mapping]] = ..., ALIGNMENT_WORD: _Optional[_Union[AlignmentWordType, _Mapping]] = ..., ALIGNMENT_LONG: _Optional[_Union[AlignmentLongType, _Mapping]] = ..., ALIGNMENT_FLOAT32_IEEE: _Optional[_Union[AlignmentFloat32IeeeType, _Mapping]] = ..., ALIGNMENT_FLOAT64_IEEE: _Optional[_Union[AlignmentFloat64IeeeType, _Mapping]] = ...) -> None: ...

class ModParType(_message.Message):
    __slots__ = ("Comment", "VERSION", "ADDR_EPK", "EPK", "SUPPLIER", "CUSTOMER", "CUSTOMER_NO", "USER", "PHONE_NO", "ECU", "CPU_TYPE", "NO_OF_INTERFACES", "ECU_CALIBRATION_OFFSET", "CALIBRATION_METHOD", "MEMORY_LAYOUT", "MEMORY_SEGMENT", "SYSTEM_CONSTANT")
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ADDR_EPK_FIELD_NUMBER: _ClassVar[int]
    EPK_FIELD_NUMBER: _ClassVar[int]
    SUPPLIER_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_NO_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    PHONE_NO_FIELD_NUMBER: _ClassVar[int]
    ECU_FIELD_NUMBER: _ClassVar[int]
    CPU_TYPE_FIELD_NUMBER: _ClassVar[int]
    NO_OF_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    ECU_CALIBRATION_OFFSET_FIELD_NUMBER: _ClassVar[int]
    CALIBRATION_METHOD_FIELD_NUMBER: _ClassVar[int]
    MEMORY_LAYOUT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_SEGMENT_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_CONSTANT_FIELD_NUMBER: _ClassVar[int]
    Comment: _shared_pb2.StringType
    VERSION: VersionType
    ADDR_EPK: _containers.RepeatedCompositeFieldContainer[AddrEpkType]
    EPK: EpkType
    SUPPLIER: SupplierType
    CUSTOMER: CustomerType
    CUSTOMER_NO: CustomerNoType
    USER: UserType
    PHONE_NO: PhoneNoType
    ECU: EcuType
    CPU_TYPE: CpuTypeType
    NO_OF_INTERFACES: NoOfInterfacesType
    ECU_CALIBRATION_OFFSET: EcuCalibrationOffsetType
    CALIBRATION_METHOD: _containers.RepeatedCompositeFieldContainer[CalibrationMethodType]
    MEMORY_LAYOUT: _containers.RepeatedCompositeFieldContainer[MemoryLayoutType]
    MEMORY_SEGMENT: _containers.RepeatedCompositeFieldContainer[MemorySegmentType]
    SYSTEM_CONSTANT: _containers.RepeatedCompositeFieldContainer[SystemConstantType]
    def __init__(self, Comment: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., VERSION: _Optional[_Union[VersionType, _Mapping]] = ..., ADDR_EPK: _Optional[_Iterable[_Union[AddrEpkType, _Mapping]]] = ..., EPK: _Optional[_Union[EpkType, _Mapping]] = ..., SUPPLIER: _Optional[_Union[SupplierType, _Mapping]] = ..., CUSTOMER: _Optional[_Union[CustomerType, _Mapping]] = ..., CUSTOMER_NO: _Optional[_Union[CustomerNoType, _Mapping]] = ..., USER: _Optional[_Union[UserType, _Mapping]] = ..., PHONE_NO: _Optional[_Union[PhoneNoType, _Mapping]] = ..., ECU: _Optional[_Union[EcuType, _Mapping]] = ..., CPU_TYPE: _Optional[_Union[CpuTypeType, _Mapping]] = ..., NO_OF_INTERFACES: _Optional[_Union[NoOfInterfacesType, _Mapping]] = ..., ECU_CALIBRATION_OFFSET: _Optional[_Union[EcuCalibrationOffsetType, _Mapping]] = ..., CALIBRATION_METHOD: _Optional[_Iterable[_Union[CalibrationMethodType, _Mapping]]] = ..., MEMORY_LAYOUT: _Optional[_Iterable[_Union[MemoryLayoutType, _Mapping]]] = ..., MEMORY_SEGMENT: _Optional[_Iterable[_Union[MemorySegmentType, _Mapping]]] = ..., SYSTEM_CONSTANT: _Optional[_Iterable[_Union[SystemConstantType, _Mapping]]] = ...) -> None: ...

class ModuleType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "A2ML", "MOD_PAR", "MOD_COMMON", "IF_DATA", "CHARACTERISTIC", "AXIS_PTS", "MEASUREMENT", "COMPU_METHOD", "COMPU_TAB", "COMPU_VTAB", "COMPU_VTAB_RANGE", "FUNCTION", "GROUP", "RECORD_LAYOUT", "VARIANT_CODING", "FRAME", "USER_RIGHTS", "UNIT")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    A2ML_FIELD_NUMBER: _ClassVar[int]
    MOD_PAR_FIELD_NUMBER: _ClassVar[int]
    MOD_COMMON_FIELD_NUMBER: _ClassVar[int]
    IF_DATA_FIELD_NUMBER: _ClassVar[int]
    CHARACTERISTIC_FIELD_NUMBER: _ClassVar[int]
    AXIS_PTS_FIELD_NUMBER: _ClassVar[int]
    MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    COMPU_METHOD_FIELD_NUMBER: _ClassVar[int]
    COMPU_TAB_FIELD_NUMBER: _ClassVar[int]
    COMPU_VTAB_FIELD_NUMBER: _ClassVar[int]
    COMPU_VTAB_RANGE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    RECORD_LAYOUT_FIELD_NUMBER: _ClassVar[int]
    VARIANT_CODING_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    USER_RIGHTS_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    A2ML: A2MLType
    MOD_PAR: ModParType
    MOD_COMMON: ModCommonType
    IF_DATA: _containers.RepeatedCompositeFieldContainer[_IF_DATA_pb2.IfDataType]
    CHARACTERISTIC: _containers.RepeatedCompositeFieldContainer[CharacteristicType]
    AXIS_PTS: _containers.RepeatedCompositeFieldContainer[AxisPtsType]
    MEASUREMENT: _containers.RepeatedCompositeFieldContainer[MeasurementType]
    COMPU_METHOD: _containers.RepeatedCompositeFieldContainer[CompuMethodType]
    COMPU_TAB: _containers.RepeatedCompositeFieldContainer[CompuTabType]
    COMPU_VTAB: _containers.RepeatedCompositeFieldContainer[CompuVTabType]
    COMPU_VTAB_RANGE: _containers.RepeatedCompositeFieldContainer[CompuVTabRangeType]
    FUNCTION: _containers.RepeatedCompositeFieldContainer[FunctionType]
    GROUP: _containers.RepeatedCompositeFieldContainer[GroupType]
    RECORD_LAYOUT: _containers.RepeatedCompositeFieldContainer[RecordLayoutType]
    VARIANT_CODING: VariantCodingType
    FRAME: FrameType
    USER_RIGHTS: _containers.RepeatedCompositeFieldContainer[UserRightsType]
    UNIT: _containers.RepeatedCompositeFieldContainer[UnitType]
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., A2ML: _Optional[_Union[A2MLType, _Mapping]] = ..., MOD_PAR: _Optional[_Union[ModParType, _Mapping]] = ..., MOD_COMMON: _Optional[_Union[ModCommonType, _Mapping]] = ..., IF_DATA: _Optional[_Iterable[_Union[_IF_DATA_pb2.IfDataType, _Mapping]]] = ..., CHARACTERISTIC: _Optional[_Iterable[_Union[CharacteristicType, _Mapping]]] = ..., AXIS_PTS: _Optional[_Iterable[_Union[AxisPtsType, _Mapping]]] = ..., MEASUREMENT: _Optional[_Iterable[_Union[MeasurementType, _Mapping]]] = ..., COMPU_METHOD: _Optional[_Iterable[_Union[CompuMethodType, _Mapping]]] = ..., COMPU_TAB: _Optional[_Iterable[_Union[CompuTabType, _Mapping]]] = ..., COMPU_VTAB: _Optional[_Iterable[_Union[CompuVTabType, _Mapping]]] = ..., COMPU_VTAB_RANGE: _Optional[_Iterable[_Union[CompuVTabRangeType, _Mapping]]] = ..., FUNCTION: _Optional[_Iterable[_Union[FunctionType, _Mapping]]] = ..., GROUP: _Optional[_Iterable[_Union[GroupType, _Mapping]]] = ..., RECORD_LAYOUT: _Optional[_Iterable[_Union[RecordLayoutType, _Mapping]]] = ..., VARIANT_CODING: _Optional[_Union[VariantCodingType, _Mapping]] = ..., FRAME: _Optional[_Union[FrameType, _Mapping]] = ..., USER_RIGHTS: _Optional[_Iterable[_Union[UserRightsType, _Mapping]]] = ..., UNIT: _Optional[_Iterable[_Union[UnitType, _Mapping]]] = ...) -> None: ...

class MonotonyType(_message.Message):
    __slots__ = ("Monotony",)
    MONOTONY_FIELD_NUMBER: _ClassVar[int]
    Monotony: str
    def __init__(self, Monotony: _Optional[str] = ...) -> None: ...

class NoAxisPtsXType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class NoAxisPtsYType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class NoAxisPtsZType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class NoOfInterfacesType(_message.Message):
    __slots__ = ("Num",)
    NUM_FIELD_NUMBER: _ClassVar[int]
    Num: _shared_pb2.IntType
    def __init__(self, Num: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class NoRescaleXType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class NoRescaleYType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class NoRescaleZType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class NumberType(_message.Message):
    __slots__ = ("Number",)
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    Number: _shared_pb2.IntType
    def __init__(self, Number: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class OffsetXType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class OffsetYType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class OffsetZType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class OutMeasurementType(_message.Message):
    __slots__ = ("Identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Identifier: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Identifier: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class PhoneNoType(_message.Message):
    __slots__ = ("TelNum",)
    TELNUM_FIELD_NUMBER: _ClassVar[int]
    TelNum: _shared_pb2.StringType
    def __init__(self, TelNum: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class PhysUnitType(_message.Message):
    __slots__ = ("Unit",)
    UNIT_FIELD_NUMBER: _ClassVar[int]
    Unit: _shared_pb2.StringType
    def __init__(self, Unit: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class ProjectNoType(_message.Message):
    __slots__ = ("ProjectNumber",)
    PROJECTNUMBER_FIELD_NUMBER: _ClassVar[int]
    ProjectNumber: _shared_pb2.IdentType
    def __init__(self, ProjectNumber: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class ProjectType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "HEADER", "MODULE")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODULE_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    HEADER: HeaderType
    MODULE: _containers.RepeatedCompositeFieldContainer[ModuleType]
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., HEADER: _Optional[_Union[HeaderType, _Mapping]] = ..., MODULE: _Optional[_Iterable[_Union[ModuleType, _Mapping]]] = ...) -> None: ...

class ReadOnlyType(_message.Message):
    __slots__ = ("Present",)
    PRESENT_FIELD_NUMBER: _ClassVar[int]
    Present: bool
    def __init__(self, Present: bool = ...) -> None: ...

class ReadWriteType(_message.Message):
    __slots__ = ("Present",)
    PRESENT_FIELD_NUMBER: _ClassVar[int]
    Present: bool
    def __init__(self, Present: bool = ...) -> None: ...

class RecordLayoutType(_message.Message):
    __slots__ = ("Name", "FNC_VALUES", "IDENTIFICATION", "AXIS_PTS_X", "AXIS_PTS_Y", "AXIS_PTS_Z", "AXIS_RESCALE_X", "AXIS_RESCALE_Y", "AXIS_RESCALE_Z", "NO_AXIS_PTS_X", "NO_AXIS_PTS_Y", "NO_AXIS_PTS_Z", "NO_RESCALE_X", "NO_RESCALE_Y", "NO_RESCALE_Z", "FIX_NO_AXIS_PTS_X", "FIX_NO_AXIS_PTS_Y", "FIX_NO_AXIS_PTS_Z", "SRC_ADDR_X", "SRC_ADDR_Y", "SRC_ADDR_Z", "RIP_ADDR_X", "RIP_ADDR_Y", "RIP_ADDR_Z", "RIP_ADDR_W", "SHIFT_OP_X", "SHIFT_OP_Y", "SHIFT_OP_Z", "OFFSET_X", "OFFSET_Y", "OFFSET_Z", "DIST_OP_X", "DIST_OP_Y", "DIST_OP_Z", "ALIGNMENT_BYTE", "ALIGNMENT_WORD", "ALIGNMENT_LONG", "ALIGNMENT_FLOAT32_IEEE", "ALIGNMENT_FLOAT64_IEEE", "RESERVED")
    NAME_FIELD_NUMBER: _ClassVar[int]
    FNC_VALUES_FIELD_NUMBER: _ClassVar[int]
    IDENTIFICATION_FIELD_NUMBER: _ClassVar[int]
    AXIS_PTS_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_PTS_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_PTS_Z_FIELD_NUMBER: _ClassVar[int]
    AXIS_RESCALE_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_RESCALE_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_RESCALE_Z_FIELD_NUMBER: _ClassVar[int]
    NO_AXIS_PTS_X_FIELD_NUMBER: _ClassVar[int]
    NO_AXIS_PTS_Y_FIELD_NUMBER: _ClassVar[int]
    NO_AXIS_PTS_Z_FIELD_NUMBER: _ClassVar[int]
    NO_RESCALE_X_FIELD_NUMBER: _ClassVar[int]
    NO_RESCALE_Y_FIELD_NUMBER: _ClassVar[int]
    NO_RESCALE_Z_FIELD_NUMBER: _ClassVar[int]
    FIX_NO_AXIS_PTS_X_FIELD_NUMBER: _ClassVar[int]
    FIX_NO_AXIS_PTS_Y_FIELD_NUMBER: _ClassVar[int]
    FIX_NO_AXIS_PTS_Z_FIELD_NUMBER: _ClassVar[int]
    SRC_ADDR_X_FIELD_NUMBER: _ClassVar[int]
    SRC_ADDR_Y_FIELD_NUMBER: _ClassVar[int]
    SRC_ADDR_Z_FIELD_NUMBER: _ClassVar[int]
    RIP_ADDR_X_FIELD_NUMBER: _ClassVar[int]
    RIP_ADDR_Y_FIELD_NUMBER: _ClassVar[int]
    RIP_ADDR_Z_FIELD_NUMBER: _ClassVar[int]
    RIP_ADDR_W_FIELD_NUMBER: _ClassVar[int]
    SHIFT_OP_X_FIELD_NUMBER: _ClassVar[int]
    SHIFT_OP_Y_FIELD_NUMBER: _ClassVar[int]
    SHIFT_OP_Z_FIELD_NUMBER: _ClassVar[int]
    OFFSET_X_FIELD_NUMBER: _ClassVar[int]
    OFFSET_Y_FIELD_NUMBER: _ClassVar[int]
    OFFSET_Z_FIELD_NUMBER: _ClassVar[int]
    DIST_OP_X_FIELD_NUMBER: _ClassVar[int]
    DIST_OP_Y_FIELD_NUMBER: _ClassVar[int]
    DIST_OP_Z_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_BYTE_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_WORD_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_LONG_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_FLOAT32_IEEE_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_FLOAT64_IEEE_FIELD_NUMBER: _ClassVar[int]
    RESERVED_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    FNC_VALUES: FncValuesType
    IDENTIFICATION: IdentificationType
    AXIS_PTS_X: AxisPtsXType
    AXIS_PTS_Y: AxisPtsYType
    AXIS_PTS_Z: AxisPtsZType
    AXIS_RESCALE_X: AxisRescaleXType
    AXIS_RESCALE_Y: AxisRescaleYType
    AXIS_RESCALE_Z: AxisRescaleZType
    NO_AXIS_PTS_X: NoAxisPtsXType
    NO_AXIS_PTS_Y: NoAxisPtsYType
    NO_AXIS_PTS_Z: NoAxisPtsZType
    NO_RESCALE_X: NoRescaleXType
    NO_RESCALE_Y: NoRescaleYType
    NO_RESCALE_Z: NoRescaleZType
    FIX_NO_AXIS_PTS_X: FixNoAxisPtsXType
    FIX_NO_AXIS_PTS_Y: FixNoAxisPtsYType
    FIX_NO_AXIS_PTS_Z: FixNoAxisPtsZType
    SRC_ADDR_X: SrcAddrXType
    SRC_ADDR_Y: SrcAddrYType
    SRC_ADDR_Z: SrcAddrZType
    RIP_ADDR_X: RipAddrXType
    RIP_ADDR_Y: RipAddrYType
    RIP_ADDR_Z: RipAddrZType
    RIP_ADDR_W: RipAddrWType
    SHIFT_OP_X: ShiftOpXType
    SHIFT_OP_Y: ShiftOpYType
    SHIFT_OP_Z: ShiftOpZType
    OFFSET_X: OffsetXType
    OFFSET_Y: OffsetYType
    OFFSET_Z: OffsetZType
    DIST_OP_X: DistOpXType
    DIST_OP_Y: DistOpYType
    DIST_OP_Z: DistOpZType
    ALIGNMENT_BYTE: AlignmentByteType
    ALIGNMENT_WORD: AlignmentWordType
    ALIGNMENT_LONG: AlignmentLongType
    ALIGNMENT_FLOAT32_IEEE: AlignmentFloat32IeeeType
    ALIGNMENT_FLOAT64_IEEE: AlignmentFloat64IeeeType
    RESERVED: _containers.RepeatedCompositeFieldContainer[ReservedType]
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., FNC_VALUES: _Optional[_Union[FncValuesType, _Mapping]] = ..., IDENTIFICATION: _Optional[_Union[IdentificationType, _Mapping]] = ..., AXIS_PTS_X: _Optional[_Union[AxisPtsXType, _Mapping]] = ..., AXIS_PTS_Y: _Optional[_Union[AxisPtsYType, _Mapping]] = ..., AXIS_PTS_Z: _Optional[_Union[AxisPtsZType, _Mapping]] = ..., AXIS_RESCALE_X: _Optional[_Union[AxisRescaleXType, _Mapping]] = ..., AXIS_RESCALE_Y: _Optional[_Union[AxisRescaleYType, _Mapping]] = ..., AXIS_RESCALE_Z: _Optional[_Union[AxisRescaleZType, _Mapping]] = ..., NO_AXIS_PTS_X: _Optional[_Union[NoAxisPtsXType, _Mapping]] = ..., NO_AXIS_PTS_Y: _Optional[_Union[NoAxisPtsYType, _Mapping]] = ..., NO_AXIS_PTS_Z: _Optional[_Union[NoAxisPtsZType, _Mapping]] = ..., NO_RESCALE_X: _Optional[_Union[NoRescaleXType, _Mapping]] = ..., NO_RESCALE_Y: _Optional[_Union[NoRescaleYType, _Mapping]] = ..., NO_RESCALE_Z: _Optional[_Union[NoRescaleZType, _Mapping]] = ..., FIX_NO_AXIS_PTS_X: _Optional[_Union[FixNoAxisPtsXType, _Mapping]] = ..., FIX_NO_AXIS_PTS_Y: _Optional[_Union[FixNoAxisPtsYType, _Mapping]] = ..., FIX_NO_AXIS_PTS_Z: _Optional[_Union[FixNoAxisPtsZType, _Mapping]] = ..., SRC_ADDR_X: _Optional[_Union[SrcAddrXType, _Mapping]] = ..., SRC_ADDR_Y: _Optional[_Union[SrcAddrYType, _Mapping]] = ..., SRC_ADDR_Z: _Optional[_Union[SrcAddrZType, _Mapping]] = ..., RIP_ADDR_X: _Optional[_Union[RipAddrXType, _Mapping]] = ..., RIP_ADDR_Y: _Optional[_Union[RipAddrYType, _Mapping]] = ..., RIP_ADDR_Z: _Optional[_Union[RipAddrZType, _Mapping]] = ..., RIP_ADDR_W: _Optional[_Union[RipAddrWType, _Mapping]] = ..., SHIFT_OP_X: _Optional[_Union[ShiftOpXType, _Mapping]] = ..., SHIFT_OP_Y: _Optional[_Union[ShiftOpYType, _Mapping]] = ..., SHIFT_OP_Z: _Optional[_Union[ShiftOpZType, _Mapping]] = ..., OFFSET_X: _Optional[_Union[OffsetXType, _Mapping]] = ..., OFFSET_Y: _Optional[_Union[OffsetYType, _Mapping]] = ..., OFFSET_Z: _Optional[_Union[OffsetZType, _Mapping]] = ..., DIST_OP_X: _Optional[_Union[DistOpXType, _Mapping]] = ..., DIST_OP_Y: _Optional[_Union[DistOpYType, _Mapping]] = ..., DIST_OP_Z: _Optional[_Union[DistOpZType, _Mapping]] = ..., ALIGNMENT_BYTE: _Optional[_Union[AlignmentByteType, _Mapping]] = ..., ALIGNMENT_WORD: _Optional[_Union[AlignmentWordType, _Mapping]] = ..., ALIGNMENT_LONG: _Optional[_Union[AlignmentLongType, _Mapping]] = ..., ALIGNMENT_FLOAT32_IEEE: _Optional[_Union[AlignmentFloat32IeeeType, _Mapping]] = ..., ALIGNMENT_FLOAT64_IEEE: _Optional[_Union[AlignmentFloat64IeeeType, _Mapping]] = ..., RESERVED: _Optional[_Iterable[_Union[ReservedType, _Mapping]]] = ...) -> None: ...

class RefCharacteristicType(_message.Message):
    __slots__ = ("Identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Identifier: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Identifier: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class RefGroupType(_message.Message):
    __slots__ = ("Identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Identifier: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Identifier: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class RefMeasurementType(_message.Message):
    __slots__ = ("Identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Identifier: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Identifier: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class RefMemorySegmentType(_message.Message):
    __slots__ = ("Name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class RefUnitType(_message.Message):
    __slots__ = ("Unit",)
    UNIT_FIELD_NUMBER: _ClassVar[int]
    Unit: _shared_pb2.IdentType
    def __init__(self, Unit: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class ReservedType(_message.Message):
    __slots__ = ("Position", "DataSize")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATASIZE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataSize: str
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataSize: _Optional[str] = ...) -> None: ...

class RightShiftType(_message.Message):
    __slots__ = ("BitCount",)
    BITCOUNT_FIELD_NUMBER: _ClassVar[int]
    BitCount: _shared_pb2.LongType
    def __init__(self, BitCount: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ...) -> None: ...

class RipAddrWType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class RipAddrXType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class RipAddrYType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class RipAddrZType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class RootNodeType(_message.Message):
    __slots__ = ("ASAP2_VERSION", "A2ML_VERSION", "PROJECT")
    ASAP2_VERSION_FIELD_NUMBER: _ClassVar[int]
    A2ML_VERSION_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    ASAP2_VERSION: ASAP2VersionType
    A2ML_VERSION: A2MLVersionType
    PROJECT: ProjectType
    def __init__(self, ASAP2_VERSION: _Optional[_Union[ASAP2VersionType, _Mapping]] = ..., A2ML_VERSION: _Optional[_Union[A2MLVersionType, _Mapping]] = ..., PROJECT: _Optional[_Union[ProjectType, _Mapping]] = ...) -> None: ...

class RootType(_message.Message):
    __slots__ = ("Present",)
    PRESENT_FIELD_NUMBER: _ClassVar[int]
    Present: bool
    def __init__(self, Present: bool = ...) -> None: ...

class ShiftOpXType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class ShiftOpYType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class ShiftOpZType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class SiExponentsType(_message.Message):
    __slots__ = ("Length", "Mass", "Time", "ElectricCurrent", "Temperature", "AmountOfSubstance", "LuminousIntensity")
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    MASS_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    ELECTRICCURRENT_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    AMOUNTOFSUBSTANCE_FIELD_NUMBER: _ClassVar[int]
    LUMINOUSINTENSITY_FIELD_NUMBER: _ClassVar[int]
    Length: _shared_pb2.IntType
    Mass: _shared_pb2.IntType
    Time: _shared_pb2.IntType
    ElectricCurrent: _shared_pb2.IntType
    Temperature: _shared_pb2.IntType
    AmountOfSubstance: _shared_pb2.IntType
    LuminousIntensity: _shared_pb2.IntType
    def __init__(self, Length: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., Mass: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., Time: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., ElectricCurrent: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., Temperature: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., AmountOfSubstance: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., LuminousIntensity: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ...) -> None: ...

class SignExtendType(_message.Message):
    __slots__ = ("Present",)
    PRESENT_FIELD_NUMBER: _ClassVar[int]
    Present: bool
    def __init__(self, Present: bool = ...) -> None: ...

class SrcAddrXType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class SrcAddrYType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class SrcAddrZType(_message.Message):
    __slots__ = ("Position", "DataType")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    Position: _shared_pb2.IntType
    DataType: DataTypeType
    def __init__(self, Position: _Optional[_Union[_shared_pb2.IntType, _Mapping]] = ..., DataType: _Optional[_Union[DataTypeType, _Mapping]] = ...) -> None: ...

class SRecLayoutType(_message.Message):
    __slots__ = ("Name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class StepSizeType(_message.Message):
    __slots__ = ("StepSize",)
    STEPSIZE_FIELD_NUMBER: _ClassVar[int]
    StepSize: _shared_pb2.FloatType
    def __init__(self, StepSize: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ...) -> None: ...

class SubFunctionType(_message.Message):
    __slots__ = ("Identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Identifier: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Identifier: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class SubGroupType(_message.Message):
    __slots__ = ("Identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    Identifier: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Identifier: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class SupplierType(_message.Message):
    __slots__ = ("Manufacturer",)
    MANUFACTURER_FIELD_NUMBER: _ClassVar[int]
    Manufacturer: _shared_pb2.StringType
    def __init__(self, Manufacturer: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class SymbolLinkType(_message.Message):
    __slots__ = ("SymbolName", "Offset")
    SYMBOLNAME_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    SymbolName: _shared_pb2.StringType
    Offset: _shared_pb2.LongType
    def __init__(self, SymbolName: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Offset: _Optional[_Union[_shared_pb2.LongType, _Mapping]] = ...) -> None: ...

class SystemConstantType(_message.Message):
    __slots__ = ("Name", "Value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.StringType
    Value: _shared_pb2.StringType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Value: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class UnitConversionType(_message.Message):
    __slots__ = ("Gradient", "Offset")
    GRADIENT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    Gradient: _shared_pb2.FloatType
    Offset: _shared_pb2.FloatType
    def __init__(self, Gradient: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ..., Offset: _Optional[_Union[_shared_pb2.FloatType, _Mapping]] = ...) -> None: ...

class UnitType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "Display", "Type", "SI_EXPONENTS", "REF_UNIT", "UNIT_CONVERSION")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SI_EXPONENTS_FIELD_NUMBER: _ClassVar[int]
    REF_UNIT_FIELD_NUMBER: _ClassVar[int]
    UNIT_CONVERSION_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    Display: _shared_pb2.StringType
    Type: str
    SI_EXPONENTS: SiExponentsType
    REF_UNIT: RefUnitType
    UNIT_CONVERSION: UnitConversionType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Display: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Type: _Optional[str] = ..., SI_EXPONENTS: _Optional[_Union[SiExponentsType, _Mapping]] = ..., REF_UNIT: _Optional[_Union[RefUnitType, _Mapping]] = ..., UNIT_CONVERSION: _Optional[_Union[UnitConversionType, _Mapping]] = ...) -> None: ...

class UserRightsType(_message.Message):
    __slots__ = ("UserLevelId", "REF_GROUP", "READ_ONLY")
    USERLEVELID_FIELD_NUMBER: _ClassVar[int]
    REF_GROUP_FIELD_NUMBER: _ClassVar[int]
    READ_ONLY_FIELD_NUMBER: _ClassVar[int]
    UserLevelId: _shared_pb2.IdentType
    REF_GROUP: _containers.RepeatedCompositeFieldContainer[RefGroupType]
    READ_ONLY: ReadOnlyType
    def __init__(self, UserLevelId: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., REF_GROUP: _Optional[_Iterable[_Union[RefGroupType, _Mapping]]] = ..., READ_ONLY: _Optional[_Union[ReadOnlyType, _Mapping]] = ...) -> None: ...

class UserType(_message.Message):
    __slots__ = ("UserName",)
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    UserName: _shared_pb2.StringType
    def __init__(self, UserName: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class VarAddressType(_message.Message):
    __slots__ = ("Address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    Address: _containers.RepeatedCompositeFieldContainer[_shared_pb2.LongType]
    def __init__(self, Address: _Optional[_Iterable[_Union[_shared_pb2.LongType, _Mapping]]] = ...) -> None: ...

class VarCharacteristicType(_message.Message):
    __slots__ = ("Name", "CriterionName", "VAR_ADDRESS")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CRITERIONNAME_FIELD_NUMBER: _ClassVar[int]
    VAR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    CriterionName: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    VAR_ADDRESS: VarAddressType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., CriterionName: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ..., VAR_ADDRESS: _Optional[_Union[VarAddressType, _Mapping]] = ...) -> None: ...

class VarCriterionType(_message.Message):
    __slots__ = ("Name", "LongIdentifier", "Value", "VAR_MEASUREMENT", "VAR_SELECTION_CHARACTERISTIC")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LONGIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VAR_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    VAR_SELECTION_CHARACTERISTIC_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    LongIdentifier: _shared_pb2.StringType
    Value: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    VAR_MEASUREMENT: VarMeasurementType
    VAR_SELECTION_CHARACTERISTIC: VarSelectionCharacteristicType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., LongIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Value: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ..., VAR_MEASUREMENT: _Optional[_Union[VarMeasurementType, _Mapping]] = ..., VAR_SELECTION_CHARACTERISTIC: _Optional[_Union[VarSelectionCharacteristicType, _Mapping]] = ...) -> None: ...

class VarForbiddenCombType(_message.Message):
    __slots__ = ("CriterionNameCriterionValue",)
    class CriterionType(_message.Message):
        __slots__ = ("CriterionName", "CriterionValue")
        CRITERIONNAME_FIELD_NUMBER: _ClassVar[int]
        CRITERIONVALUE_FIELD_NUMBER: _ClassVar[int]
        CriterionName: _shared_pb2.IdentType
        CriterionValue: _shared_pb2.IdentType
        def __init__(self, CriterionName: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ..., CriterionValue: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...
    CRITERIONNAMECRITERIONVALUE_FIELD_NUMBER: _ClassVar[int]
    CriterionNameCriterionValue: _containers.RepeatedCompositeFieldContainer[VarForbiddenCombType.CriterionType]
    def __init__(self, CriterionNameCriterionValue: _Optional[_Iterable[_Union[VarForbiddenCombType.CriterionType, _Mapping]]] = ...) -> None: ...

class VariantCodingType(_message.Message):
    __slots__ = ("VAR_SEPARATOR", "VAR_NAMING", "VAR_CRITERION", "VAR_FORBIDDEN_COMB", "VAR_CHARACTERISTIC")
    VAR_SEPARATOR_FIELD_NUMBER: _ClassVar[int]
    VAR_NAMING_FIELD_NUMBER: _ClassVar[int]
    VAR_CRITERION_FIELD_NUMBER: _ClassVar[int]
    VAR_FORBIDDEN_COMB_FIELD_NUMBER: _ClassVar[int]
    VAR_CHARACTERISTIC_FIELD_NUMBER: _ClassVar[int]
    VAR_SEPARATOR: VarSeparatorType
    VAR_NAMING: VarNamingType
    VAR_CRITERION: _containers.RepeatedCompositeFieldContainer[VarCriterionType]
    VAR_FORBIDDEN_COMB: _containers.RepeatedCompositeFieldContainer[VarForbiddenCombType]
    VAR_CHARACTERISTIC: _containers.RepeatedCompositeFieldContainer[VarCharacteristicType]
    def __init__(self, VAR_SEPARATOR: _Optional[_Union[VarSeparatorType, _Mapping]] = ..., VAR_NAMING: _Optional[_Union[VarNamingType, _Mapping]] = ..., VAR_CRITERION: _Optional[_Iterable[_Union[VarCriterionType, _Mapping]]] = ..., VAR_FORBIDDEN_COMB: _Optional[_Iterable[_Union[VarForbiddenCombType, _Mapping]]] = ..., VAR_CHARACTERISTIC: _Optional[_Iterable[_Union[VarCharacteristicType, _Mapping]]] = ...) -> None: ...

class VarMeasurementType(_message.Message):
    __slots__ = ("Name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class VarNamingType(_message.Message):
    __slots__ = ("Tag",)
    TAG_FIELD_NUMBER: _ClassVar[int]
    Tag: str
    def __init__(self, Tag: _Optional[str] = ...) -> None: ...

class VarSelectionCharacteristicType(_message.Message):
    __slots__ = ("Name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    Name: _shared_pb2.IdentType
    def __init__(self, Name: _Optional[_Union[_shared_pb2.IdentType, _Mapping]] = ...) -> None: ...

class VarSeparatorType(_message.Message):
    __slots__ = ("Separator",)
    SEPARATOR_FIELD_NUMBER: _ClassVar[int]
    Separator: _shared_pb2.StringType
    def __init__(self, Separator: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class VersionType(_message.Message):
    __slots__ = ("VersionIdentifier",)
    VERSIONIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    VersionIdentifier: _shared_pb2.StringType
    def __init__(self, VersionIdentifier: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ...) -> None: ...

class VirtualCharacteristicType(_message.Message):
    __slots__ = ("Formula", "Characteristic")
    FORMULA_FIELD_NUMBER: _ClassVar[int]
    CHARACTERISTIC_FIELD_NUMBER: _ClassVar[int]
    Formula: _shared_pb2.StringType
    Characteristic: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, Formula: _Optional[_Union[_shared_pb2.StringType, _Mapping]] = ..., Characteristic: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...

class VirtualType(_message.Message):
    __slots__ = ("MeasuringChannel",)
    MEASURINGCHANNEL_FIELD_NUMBER: _ClassVar[int]
    MeasuringChannel: _containers.RepeatedCompositeFieldContainer[_shared_pb2.IdentType]
    def __init__(self, MeasuringChannel: _Optional[_Iterable[_Union[_shared_pb2.IdentType, _Mapping]]] = ...) -> None: ...
