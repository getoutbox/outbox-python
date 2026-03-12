import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InboundEvent(_message.Message):
    __slots__ = ("messages", "deliveries", "receipts", "typings")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    DELIVERIES_FIELD_NUMBER: _ClassVar[int]
    RECEIPTS_FIELD_NUMBER: _ClassVar[int]
    TYPINGS_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[InboundMessage]
    deliveries: _containers.RepeatedCompositeFieldContainer[InboundDelivery]
    receipts: _containers.RepeatedCompositeFieldContainer[InboundReceipt]
    typings: _containers.RepeatedCompositeFieldContainer[InboundTyping]
    def __init__(self, messages: _Optional[_Iterable[_Union[InboundMessage, _Mapping]]] = ..., deliveries: _Optional[_Iterable[_Union[InboundDelivery, _Mapping]]] = ..., receipts: _Optional[_Iterable[_Union[InboundReceipt, _Mapping]]] = ..., typings: _Optional[_Iterable[_Union[InboundTyping, _Mapping]]] = ...) -> None: ...

class InboundMessage(_message.Message):
    __slots__ = ("external_id", "external_type", "external_message_id", "parts", "metadata", "group_id", "reply_to_external_id", "replaces_external_id", "deletion_scope", "edit_number")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    REPLACES_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    DELETION_SCOPE_FIELD_NUMBER: _ClassVar[int]
    EDIT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    external_id: str
    external_type: str
    external_message_id: str
    parts: _containers.RepeatedCompositeFieldContainer[InboundPart]
    metadata: _containers.ScalarMap[str, str]
    group_id: str
    reply_to_external_id: str
    replaces_external_id: str
    deletion_scope: str
    edit_number: int
    def __init__(self, external_id: _Optional[str] = ..., external_type: _Optional[str] = ..., external_message_id: _Optional[str] = ..., parts: _Optional[_Iterable[_Union[InboundPart, _Mapping]]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., group_id: _Optional[str] = ..., reply_to_external_id: _Optional[str] = ..., replaces_external_id: _Optional[str] = ..., deletion_scope: _Optional[str] = ..., edit_number: _Optional[int] = ...) -> None: ...

class InboundPart(_message.Message):
    __slots__ = ("content_type", "disposition", "url", "content", "filename")
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISPOSITION_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    content_type: str
    disposition: str
    url: str
    content: bytes
    filename: str
    def __init__(self, content_type: _Optional[str] = ..., disposition: _Optional[str] = ..., url: _Optional[str] = ..., content: _Optional[bytes] = ..., filename: _Optional[str] = ...) -> None: ...

class InboundDelivery(_message.Message):
    __slots__ = ("external_message_id", "status", "error_code", "error_message")
    EXTERNAL_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    external_message_id: str
    status: str
    error_code: str
    error_message: str
    def __init__(self, external_message_id: _Optional[str] = ..., status: _Optional[str] = ..., error_code: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class InboundReceipt(_message.Message):
    __slots__ = ("external_id", "external_type", "external_message_ids", "timestamp")
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    external_id: str
    external_type: str
    external_message_ids: _containers.RepeatedScalarFieldContainer[str]
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, external_id: _Optional[str] = ..., external_type: _Optional[str] = ..., external_message_ids: _Optional[_Iterable[str]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class InboundTyping(_message.Message):
    __slots__ = ("external_id", "external_type", "typing", "timestamp", "content_type")
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPING_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    external_id: str
    external_type: str
    typing: bool
    timestamp: _timestamp_pb2.Timestamp
    content_type: str
    def __init__(self, external_id: _Optional[str] = ..., external_type: _Optional[str] = ..., typing: _Optional[bool] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., content_type: _Optional[str] = ...) -> None: ...
