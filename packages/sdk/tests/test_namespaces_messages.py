"""Tests for MessagesNamespace using mocked gRPC clients."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from outbox.v1 import message_pb2
from outbox_sdk._enums import MessageDeletionScope, MessageDeliveryStatus, MessageDirection
from outbox_sdk._types import MessagePart
from outbox_sdk.namespaces._messages import ListMessagesResult, MessagesNamespace, SendMessageResult


def _make_message(name: str = "messages/msg-1", recipient: str = "accounts/recip-1") -> message_pb2.Message:
    m = message_pb2.Message()
    m.name = name
    m.recipient = recipient
    m.direction = message_pb2.Message.Direction.DIRECTION_OUTBOUND
    return m


@pytest.fixture
def mock_msg_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def ns(mock_msg_client: AsyncMock) -> MessagesNamespace:
    with patch("outbox_sdk.namespaces._messages.MessageServiceClient") as MockClient:
        MockClient.return_value = mock_msg_client
        return MessagesNamespace("http://localhost:8080")


@pytest.mark.asyncio
async def test_send_success(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.CreateMessageResponse()
    resp.message.CopyFrom(_make_message())
    resp.delivery.message = "messages/msg-1"
    resp.delivery.status = message_pb2.MessageDelivery.Status.STATUS_DELIVERED
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    result = await ns.send(
        connector_id="conn-1",
        account_id="acc-1",
        parts=[MessagePart.text("Hello")],
    )

    assert isinstance(result, SendMessageResult)
    assert result.message.id == "msg-1"
    assert result.message.direction == MessageDirection.OUTBOUND
    assert result.delivery is not None
    assert result.delivery.status == MessageDeliveryStatus.DELIVERED


@pytest.mark.asyncio
async def test_send_without_delivery(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.CreateMessageResponse()
    resp.message.CopyFrom(_make_message())
    # No delivery field set
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    result = await ns.send(
        connector_id="conn-1",
        account_id="acc-1",
        parts=[MessagePart.text("Hello")],
    )

    assert result.delivery is None


@pytest.mark.asyncio
async def test_send_empty_response_raises(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.CreateMessageResponse()
    # No message set
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty message"):
        await ns.send(
            connector_id="conn-1",
            account_id="acc-1",
            parts=[MessagePart.text("Hello")],
        )


@pytest.mark.asyncio
async def test_send_auto_generates_request_id(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.CreateMessageResponse()
    resp.message.CopyFrom(_make_message())
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    await ns.send(connector_id="conn-1", account_id="acc-1", parts=[MessagePart.text("Hi")])

    call = mock_msg_client.create_message.call_args[0][0]
    assert call.request_id != ""


@pytest.mark.asyncio
async def test_send_uses_provided_request_id(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.CreateMessageResponse()
    resp.message.CopyFrom(_make_message())
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    await ns.send(
        connector_id="conn-1",
        account_id="acc-1",
        parts=[MessagePart.text("Hi")],
        request_id="my-id-123",
    )

    call = mock_msg_client.create_message.call_args[0][0]
    assert call.request_id == "my-id-123"


@pytest.mark.asyncio
async def test_send_builds_correct_proto(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.CreateMessageResponse()
    resp.message.CopyFrom(_make_message())
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    await ns.send(
        connector_id="conn-1",
        account_id="acc-1",
        parts=[MessagePart.text("Hello")],
        reply_to_message_id="parent-msg",
        group_id="grp-1",
        metadata={"key": "val"},
    )

    req = mock_msg_client.create_message.call_args[0][0]
    assert req.connector == "connectors/conn-1"
    assert req.message.recipient == "accounts/acc-1"
    assert req.message.reply_to == "messages/parent-msg"
    assert req.message.group_id == "grp-1"
    assert req.message.metadata["key"] == "val"
    assert req.message.parts[0].content == b"Hello"


@pytest.mark.asyncio
async def test_update_success(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.UpdateMessageResponse()
    resp.message.CopyFrom(_make_message("messages/msg-1"))
    mock_msg_client.update_message = AsyncMock(return_value=resp)

    result = await ns.update(id_="msg-1", parts=[MessagePart.text("Updated")])

    assert result.id == "msg-1"


@pytest.mark.asyncio
async def test_update_empty_response_raises(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.UpdateMessageResponse()
    mock_msg_client.update_message = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty message"):
        await ns.update(id_="msg-1", parts=[MessagePart.text("Updated")])


@pytest.mark.asyncio
async def test_delete_success(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.DeleteMessageResponse()
    resp.message.CopyFrom(_make_message("messages/msg-1"))
    mock_msg_client.delete_message = AsyncMock(return_value=resp)

    result = await ns.delete(id_="msg-1", deletion_scope=MessageDeletionScope.FOR_SENDER)

    assert result.id == "msg-1"
    req = mock_msg_client.delete_message.call_args[0][0]
    assert req.name == "messages/msg-1"
    assert req.scope == message_pb2.Message.DeletionScope.DELETION_SCOPE_FOR_SENDER


@pytest.mark.asyncio
async def test_delete_empty_response_raises(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.DeleteMessageResponse()
    mock_msg_client.delete_message = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty message"):
        await ns.delete(id_="msg-1", deletion_scope=MessageDeletionScope.FOR_SENDER)


@pytest.mark.asyncio
async def test_list_pagination(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.ListMessagesResponse()
    resp.messages.append(_make_message("messages/msg-1"))
    resp.messages.append(_make_message("messages/msg-2"))
    resp.next_page_token = "tok-abc"
    resp.total_size = 10
    mock_msg_client.list_messages = AsyncMock(return_value=resp)

    result = await ns.list(connector_id="conn-1", page_size=2)

    assert isinstance(result, ListMessagesResult)
    assert len(result.items) == 2
    assert result.items[0].id == "msg-1"
    assert result.items[1].id == "msg-2"
    assert result.next_page_token == "tok-abc"
    assert result.total_size == 10

    req = mock_msg_client.list_messages.call_args[0][0]
    assert req.parent == "connectors/conn-1"
    assert req.page_size == 2


@pytest.mark.asyncio
async def test_list_empty_next_page_token(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.ListMessagesResponse()
    resp.next_page_token = ""
    mock_msg_client.list_messages = AsyncMock(return_value=resp)

    result = await ns.list(connector_id="conn-1")

    assert result.next_page_token is None


@pytest.mark.asyncio
async def test_mark_read(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.SendReadReceiptResponse()
    mock_msg_client.send_read_receipt = AsyncMock(return_value=resp)

    await ns.mark_read(connector_id="conn-1", account_id="acc-1", messages=["msg-1", "msg-2"])

    req = mock_msg_client.send_read_receipt.call_args[0][0]
    assert req.connector == "connectors/conn-1"
    assert req.account == "accounts/acc-1"
    assert list(req.messages) == ["messages/msg-1", "messages/msg-2"]


@pytest.mark.asyncio
async def test_typing(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.SendTypingIndicatorResponse()
    mock_msg_client.send_typing_indicator = AsyncMock(return_value=resp)

    await ns.typing(connector_id="conn-1", account_id="acc-1", typing=True)

    req = mock_msg_client.send_typing_indicator.call_args[0][0]
    assert req.connector == "connectors/conn-1"
    assert req.account == "accounts/acc-1"
    assert req.typing is True


@pytest.mark.asyncio
async def test_typing_indicator_context_manager(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.SendTypingIndicatorResponse()
    mock_msg_client.send_typing_indicator = AsyncMock(return_value=resp)

    async with ns.typing_indicator(connector_id="conn-1", account_id="acc-1"):
        pass

    assert mock_msg_client.send_typing_indicator.call_count == 2
    first_req = mock_msg_client.send_typing_indicator.call_args_list[0][0][0]
    second_req = mock_msg_client.send_typing_indicator.call_args_list[1][0][0]
    assert first_req.typing is True
    assert second_req.typing is False


@pytest.mark.asyncio
async def test_typing_indicator_sends_false_on_exception(
    ns: MessagesNamespace, mock_msg_client: AsyncMock
) -> None:
    resp = message_pb2.SendTypingIndicatorResponse()
    mock_msg_client.send_typing_indicator = AsyncMock(return_value=resp)

    with pytest.raises(ValueError):
        async with ns.typing_indicator(connector_id="conn-1", account_id="acc-1"):
            raise ValueError("test error")

    # typing(False) must still be sent even on exception
    assert mock_msg_client.send_typing_indicator.call_count == 2
    last_req = mock_msg_client.send_typing_indicator.call_args_list[1][0][0]
    assert last_req.typing is False


@pytest.mark.asyncio
async def test_history(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.ListMessagesResponse()
    resp.messages.append(_make_message("messages/msg-1"))
    mock_msg_client.list_messages = AsyncMock(return_value=resp)

    result = await ns.history(connector_id="conn-1", account_id="acc-1")

    req = mock_msg_client.list_messages.call_args[0][0]
    assert "accounts/acc-1" in req.filter
    assert req.order_by == "create_time asc"
    assert len(result.items) == 1


@pytest.mark.asyncio
async def test_send_with_empty_metadata_dict(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.CreateMessageResponse()
    resp.message.CopyFrom(_make_message())
    resp.delivery.message = "messages/msg-1"
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    await ns.send(
        connector_id="conn-1",
        account_id="acc-1",
        parts=[MessagePart.text("Hello")],
        metadata={},
    )

    req = mock_msg_client.create_message.call_args[0][0]
    assert dict(req.message.metadata) == {}


@pytest.mark.asyncio
async def test_send_with_group_id_empty_string(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.CreateMessageResponse()
    resp.message.CopyFrom(_make_message())
    resp.delivery.message = "messages/msg-1"
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    await ns.send(
        connector_id="conn-1",
        account_id="acc-1",
        parts=[MessagePart.text("Hello")],
        group_id="",
    )

    req = mock_msg_client.create_message.call_args[0][0]
    # empty string group_id is set (not skipped), since we pass it explicitly
    assert req.message.group_id == ""


@pytest.mark.asyncio
async def test_send_with_reply_to_none_omits_field(
    ns: MessagesNamespace, mock_msg_client: AsyncMock
) -> None:
    resp = message_pb2.CreateMessageResponse()
    resp.message.CopyFrom(_make_message())
    resp.delivery.message = "messages/msg-1"
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    await ns.send(
        connector_id="conn-1",
        account_id="acc-1",
        parts=[MessagePart.text("Hello")],
        reply_to_message_id=None,
    )

    req = mock_msg_client.create_message.call_args[0][0]
    assert req.message.reply_to == ""


@pytest.mark.asyncio
async def test_send_with_multiple_metadata_keys(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.CreateMessageResponse()
    resp.message.CopyFrom(_make_message())
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    await ns.send(
        connector_id="conn-1",
        account_id="acc-1",
        parts=[MessagePart.text("Hello")],
        metadata={"key1": "val1", "key2": "val2", "priority": "high"},
    )

    req = mock_msg_client.create_message.call_args[0][0]
    assert len(req.message.metadata) == 3
    assert req.message.metadata["key1"] == "val1"
    assert req.message.metadata["priority"] == "high"


@pytest.mark.asyncio
async def test_send_all_optional_params(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.CreateMessageResponse()
    resp.message.CopyFrom(_make_message())
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    await ns.send(
        connector_id="conn-1",
        account_id="acc-1",
        parts=[MessagePart.text("Hello")],
        reply_to_message_id="msg-parent",
        group_id="group-xyz",
        metadata={"type": "response"},
        request_id="req-custom",
    )

    req = mock_msg_client.create_message.call_args[0][0]
    assert req.connector == "connectors/conn-1"
    assert req.message.reply_to == "messages/msg-parent"
    assert req.message.group_id == "group-xyz"
    assert req.message.metadata["type"] == "response"
    assert req.request_id == "req-custom"


@pytest.mark.asyncio
async def test_send_minimal_params_sets_no_optional_fields(
    ns: MessagesNamespace, mock_msg_client: AsyncMock
) -> None:
    resp = message_pb2.CreateMessageResponse()
    resp.message.CopyFrom(_make_message())
    mock_msg_client.create_message = AsyncMock(return_value=resp)

    await ns.send(
        connector_id="conn-1",
        account_id="acc-1",
        parts=[MessagePart.text("Minimal")],
    )

    req = mock_msg_client.create_message.call_args[0][0]
    assert req.message.reply_to == ""
    assert req.message.group_id == ""
    assert len(req.message.metadata) == 0


@pytest.mark.asyncio
async def test_update_field_mask_with_parts(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.UpdateMessageResponse()
    resp.message.CopyFrom(_make_message())
    mock_msg_client.update_message = AsyncMock(return_value=resp)

    await ns.update(id_="msg-1", parts=[MessagePart.text("Updated")])

    req = mock_msg_client.update_message.call_args[0][0]
    assert "parts" in list(req.update_mask.paths)


@pytest.mark.asyncio
async def test_update_field_mask_without_parts(ns: MessagesNamespace, mock_msg_client: AsyncMock) -> None:
    resp = message_pb2.UpdateMessageResponse()
    resp.message.CopyFrom(_make_message())
    mock_msg_client.update_message = AsyncMock(return_value=resp)

    await ns.update(id_="msg-1", metadata={"key": "val"})

    req = mock_msg_client.update_message.call_args[0][0]
    assert "parts" not in list(req.update_mask.paths)
    assert "metadata" in list(req.update_mask.paths)
