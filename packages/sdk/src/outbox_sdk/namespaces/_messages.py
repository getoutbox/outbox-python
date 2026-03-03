# packages/sdk/src/outbox_sdk/namespaces/_messages.py
from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from google.protobuf.field_mask_pb2 import FieldMask
from outbox.v1.message_connect import MessageServiceClient
from outbox.v1.message_pb2 import (
    CreateMessageRequest,
    DeleteMessageRequest,
    ListMessagesRequest,
    SendReadReceiptRequest,
    SendTypingIndicatorRequest,
    UpdateMessageRequest,
)
from outbox.v1.message_pb2 import (
    Message as ProtoMessage,
)
from outbox.v1.message_pb2 import (
    MessagePart as ProtoMessagePart,
)
from outbox_sdk._field_mask import derive_field_mask
from outbox_sdk._mappers import map_message, map_message_delivery
from outbox_sdk._resource_names import account_name, connector_name, message_name

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from connectrpc.interceptor import Interceptor
    from outbox_sdk._enums import MessageDeletionScope
    from outbox_sdk._types import Message, MessageDelivery, MessagePart


@dataclass
class SendMessageResult:
    message: Message
    delivery: MessageDelivery | None


@dataclass
class ListMessagesResult:
    items: list[Message]
    next_page_token: str | None
    total_size: int


class MessagesNamespace:
    def __init__(self, base_url: str, interceptors: tuple[Interceptor, ...] = ()) -> None:  # type: ignore[reportUnknownParameterType]
        self._client = MessageServiceClient(base_url, interceptors=interceptors)

    async def close(self) -> None:
        await self._client.close()

    async def send(
        self,
        *,
        connector_id: str,
        account_id: str,
        parts: list[MessagePart],
        reply_to_message_id: str | None = None,
        group_id: str | None = None,
        metadata: dict[str, str] | None = None,
        request_id: str | None = None,
    ) -> SendMessageResult:
        if request_id is None:
            request_id = str(uuid.uuid4())

        proto_parts: list[ProtoMessagePart] = []
        for p in parts:
            pp = ProtoMessagePart(
                content_type=p.content_type,
                disposition=cast("ProtoMessagePart.Disposition", p.disposition),
            )
            if p.content is not None:
                pp.content = p.content
            if p.url is not None:
                pp.url = p.url
            if p.filename is not None:
                pp.filename = p.filename
            proto_parts.append(pp)

        msg = ProtoMessage(
            parts=proto_parts,
            recipient=account_name(account_id),
        )
        if reply_to_message_id is not None:
            msg.reply_to = message_name(reply_to_message_id)
        if group_id is not None:
            msg.group_id = group_id
        if metadata is not None:
            msg.metadata.update(metadata)

        req = CreateMessageRequest(
            connector=connector_name(connector_id),
            message=msg,
            request_id=request_id,
        )
        res = await self._client.create_message(req)
        if not res.HasField("message"):
            err = "send: server returned empty message"
            raise RuntimeError(err)
        return SendMessageResult(
            message=map_message(res.message),
            delivery=map_message_delivery(res.delivery) if res.HasField("delivery") else None,
        )

    async def update(
        self,
        *,
        id_: str,
        parts: list[MessagePart] | None = None,
        metadata: dict[str, str] | None = None,
        request_id: str = "",
    ) -> Message:
        fields = {"parts": parts, "metadata": metadata}
        msg = ProtoMessage(name=message_name(id_))
        if parts is not None:
            for p in parts:
                pp = ProtoMessagePart(
                    content_type=p.content_type,
                    disposition=cast("ProtoMessagePart.Disposition", p.disposition),
                )
                if p.content is not None:
                    pp.content = p.content
                if p.url is not None:
                    pp.url = p.url
                if p.filename is not None:
                    pp.filename = p.filename
                msg.parts.append(pp)
        if metadata is not None:
            msg.metadata.update(metadata)

        req = UpdateMessageRequest(
            message=msg,
            update_mask=FieldMask(paths=derive_field_mask(fields)),
            request_id=request_id,
        )
        res = await self._client.update_message(req)
        if not res.HasField("message"):
            err = "update: server returned empty message"
            raise RuntimeError(err)
        return map_message(res.message)

    async def delete(
        self,
        *,
        id_: str,
        deletion_scope: MessageDeletionScope,
        request_id: str = "",
    ) -> Message:
        req = DeleteMessageRequest(
            name=message_name(id_),
            scope=cast("ProtoMessage.DeletionScope", deletion_scope),
            request_id=request_id,
        )
        res = await self._client.delete_message(req)
        if not res.HasField("message"):
            err = "delete: server returned empty message"
            raise RuntimeError(err)
        return map_message(res.message)

    async def list(
        self,
        *,
        connector_id: str,
        filter_: str = "",
        order_by: str = "",
        page_size: int = 0,
        page_token: str = "",
    ) -> ListMessagesResult:
        req = ListMessagesRequest(
            parent=connector_name(connector_id),
            filter=filter_,
            order_by=order_by,
            page_size=page_size,
            page_token=page_token,
        )
        res = await self._client.list_messages(req)
        return ListMessagesResult(
            items=[map_message(m) for m in res.messages],
            next_page_token=res.next_page_token or None,
            total_size=res.total_size,
        )

    async def mark_read(
        self,
        *,
        connector_id: str,
        account_id: str,
        messages: list[str],
    ) -> None:
        req = SendReadReceiptRequest(
            connector=connector_name(connector_id),
            account=account_name(account_id),
            messages=[message_name(mid) for mid in messages],
        )
        await self._client.send_read_receipt(req)

    async def typing(
        self,
        *,
        connector_id: str,
        account_id: str,
        typing: bool,
    ) -> None:
        req = SendTypingIndicatorRequest(
            connector=connector_name(connector_id),
            account=account_name(account_id),
            typing=typing,
        )
        await self._client.send_typing_indicator(req)

    @asynccontextmanager
    async def typing_indicator(
        self,
        *,
        connector_id: str,
        account_id: str,
    ) -> AsyncIterator[None]:
        """Async context manager that sends typing(True) on enter and typing(False) on exit."""
        await self.typing(connector_id=connector_id, account_id=account_id, typing=True)
        try:
            yield
        finally:
            await self.typing(connector_id=connector_id, account_id=account_id, typing=False)

    async def history(
        self,
        *,
        connector_id: str,
        account_id: str,
        page_size: int = 0,
        page_token: str = "",
    ) -> ListMessagesResult:
        """List messages in a conversation with an account."""
        name = account_name(account_id)
        return await self.list(
            connector_id=connector_id,
            filter_=f'account.name == "{name}" || recipient == "{name}"',
            order_by="create_time asc",
            page_size=page_size,
            page_token=page_token,
        )
