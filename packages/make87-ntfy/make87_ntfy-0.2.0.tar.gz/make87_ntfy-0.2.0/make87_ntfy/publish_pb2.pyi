from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessagePayload(_message.Message):
    __slots__ = ("header", "topic", "message", "title", "tags", "priority", "actions", "click", "attach", "markdown", "icon", "filename", "delay", "email", "call")
    class Priority(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[MessagePayload.Priority]
        PRIORITY_MIN: _ClassVar[MessagePayload.Priority]
        PRIORITY_LOW: _ClassVar[MessagePayload.Priority]
        PRIORITY_DEFAULT: _ClassVar[MessagePayload.Priority]
        PRIORITY_HIGH: _ClassVar[MessagePayload.Priority]
        PRIORITY_MAX: _ClassVar[MessagePayload.Priority]
    UNKNOWN: MessagePayload.Priority
    PRIORITY_MIN: MessagePayload.Priority
    PRIORITY_LOW: MessagePayload.Priority
    PRIORITY_DEFAULT: MessagePayload.Priority
    PRIORITY_HIGH: MessagePayload.Priority
    PRIORITY_MAX: MessagePayload.Priority
    class Action(_message.Message):
        __slots__ = ("label", "clear", "view", "broadcast", "http")
        LABEL_FIELD_NUMBER: _ClassVar[int]
        CLEAR_FIELD_NUMBER: _ClassVar[int]
        VIEW_FIELD_NUMBER: _ClassVar[int]
        BROADCAST_FIELD_NUMBER: _ClassVar[int]
        HTTP_FIELD_NUMBER: _ClassVar[int]
        label: str
        clear: bool
        view: MessagePayload.ViewAction
        broadcast: MessagePayload.BroadcastAction
        http: MessagePayload.HttpAction
        def __init__(self, label: _Optional[str] = ..., clear: bool = ..., view: _Optional[_Union[MessagePayload.ViewAction, _Mapping]] = ..., broadcast: _Optional[_Union[MessagePayload.BroadcastAction, _Mapping]] = ..., http: _Optional[_Union[MessagePayload.HttpAction, _Mapping]] = ...) -> None: ...
    class ViewAction(_message.Message):
        __slots__ = ("url",)
        URL_FIELD_NUMBER: _ClassVar[int]
        url: str
        def __init__(self, url: _Optional[str] = ...) -> None: ...
    class BroadcastAction(_message.Message):
        __slots__ = ("extras",)
        class ExtrasEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        EXTRAS_FIELD_NUMBER: _ClassVar[int]
        extras: _containers.ScalarMap[str, str]
        def __init__(self, extras: _Optional[_Mapping[str, str]] = ...) -> None: ...
    class HttpAction(_message.Message):
        __slots__ = ("url", "method", "headers", "body")
        class HeadersEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        URL_FIELD_NUMBER: _ClassVar[int]
        METHOD_FIELD_NUMBER: _ClassVar[int]
        HEADERS_FIELD_NUMBER: _ClassVar[int]
        BODY_FIELD_NUMBER: _ClassVar[int]
        url: str
        method: str
        headers: _containers.ScalarMap[str, str]
        body: str
        def __init__(self, url: _Optional[str] = ..., method: _Optional[str] = ..., headers: _Optional[_Mapping[str, str]] = ..., body: _Optional[str] = ...) -> None: ...
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    CLICK_FIELD_NUMBER: _ClassVar[int]
    ATTACH_FIELD_NUMBER: _ClassVar[int]
    MARKDOWN_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    CALL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    topic: str
    message: str
    title: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    priority: MessagePayload.Priority
    actions: _containers.RepeatedCompositeFieldContainer[MessagePayload.Action]
    click: str
    attach: str
    markdown: bool
    icon: str
    filename: str
    delay: str
    email: str
    call: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., topic: _Optional[str] = ..., message: _Optional[str] = ..., title: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., priority: _Optional[_Union[MessagePayload.Priority, str]] = ..., actions: _Optional[_Iterable[_Union[MessagePayload.Action, _Mapping]]] = ..., click: _Optional[str] = ..., attach: _Optional[str] = ..., markdown: bool = ..., icon: _Optional[str] = ..., filename: _Optional[str] = ..., delay: _Optional[str] = ..., email: _Optional[str] = ..., call: _Optional[str] = ...) -> None: ...
