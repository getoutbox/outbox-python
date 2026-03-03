import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import resource_pb2 as _resource_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Channel(_message.Message):
    __slots__ = ("name", "capabilities", "create_time")
    class Capabilities(_message.Message):
        __slots__ = ("groups", "reactions", "edits", "deletions", "read_receipts", "typing_indicators", "supported_content_types")
        GROUPS_FIELD_NUMBER: _ClassVar[int]
        REACTIONS_FIELD_NUMBER: _ClassVar[int]
        EDITS_FIELD_NUMBER: _ClassVar[int]
        DELETIONS_FIELD_NUMBER: _ClassVar[int]
        READ_RECEIPTS_FIELD_NUMBER: _ClassVar[int]
        TYPING_INDICATORS_FIELD_NUMBER: _ClassVar[int]
        SUPPORTED_CONTENT_TYPES_FIELD_NUMBER: _ClassVar[int]
        groups: bool
        reactions: bool
        edits: bool
        deletions: bool
        read_receipts: bool
        typing_indicators: bool
        supported_content_types: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, groups: _Optional[bool] = ..., reactions: _Optional[bool] = ..., edits: _Optional[bool] = ..., deletions: _Optional[bool] = ..., read_receipts: _Optional[bool] = ..., typing_indicators: _Optional[bool] = ..., supported_content_types: _Optional[_Iterable[str]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    capabilities: Channel.Capabilities
    create_time: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., capabilities: _Optional[_Union[Channel.Capabilities, _Mapping]] = ..., create_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListChannelsRequest(_message.Message):
    __slots__ = ("page_size", "page_token")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListChannelsResponse(_message.Message):
    __slots__ = ("channels", "next_page_token", "total_size")
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedCompositeFieldContainer[Channel]
    next_page_token: str
    total_size: int
    def __init__(self, channels: _Optional[_Iterable[_Union[Channel, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class GetChannelRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetChannelResponse(_message.Message):
    __slots__ = ("channel",)
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    channel: Channel
    def __init__(self, channel: _Optional[_Union[Channel, _Mapping]] = ...) -> None: ...
