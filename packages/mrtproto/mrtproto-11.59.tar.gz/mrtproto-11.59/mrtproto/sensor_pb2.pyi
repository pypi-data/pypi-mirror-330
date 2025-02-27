from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Range(_message.Message):
    __slots__ = ("ttag_system", "ttag_steady_ns", "type", "range_m", "range_uncertainty_m", "field_of_view_deg")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Range.Type]
        ULTRASOUND: _ClassVar[Range.Type]
        INFRARED: _ClassVar[Range.Type]
        LASER: _ClassVar[Range.Type]
    UNKNOWN: Range.Type
    ULTRASOUND: Range.Type
    INFRARED: Range.Type
    LASER: Range.Type
    TTAG_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    TTAG_STEADY_NS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    RANGE_M_FIELD_NUMBER: _ClassVar[int]
    RANGE_UNCERTAINTY_M_FIELD_NUMBER: _ClassVar[int]
    FIELD_OF_VIEW_DEG_FIELD_NUMBER: _ClassVar[int]
    ttag_system: _timestamp_pb2.Timestamp
    ttag_steady_ns: int
    type: Range.Type
    range_m: float
    range_uncertainty_m: float
    field_of_view_deg: float
    def __init__(self, ttag_system: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., ttag_steady_ns: _Optional[int] = ..., type: _Optional[_Union[Range.Type, str]] = ..., range_m: _Optional[float] = ..., range_uncertainty_m: _Optional[float] = ..., field_of_view_deg: _Optional[float] = ...) -> None: ...
