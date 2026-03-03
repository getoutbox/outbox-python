"""Tests for ChannelsNamespace using mocked gRPC clients."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from google.protobuf.timestamp_pb2 import Timestamp
from outbox.v1 import channel_pb2
from outbox_sdk._types import Channel, ChannelCapabilities
from outbox_sdk.namespaces._channels import ChannelsNamespace, ListChannelsResult


def _make_channel(name: str = "channels/whatsapp") -> channel_pb2.Channel:
    c = channel_pb2.Channel()
    c.name = name
    return c


def _make_channel_with_caps(
    name: str = "channels/whatsapp",
    *,
    groups: bool = False,
    reactions: bool = False,
    edits: bool = False,
    deletions: bool = False,
    read_receipts: bool = False,
    typing_indicators: bool = False,
    supported_content_types: list[str] | None = None,
) -> channel_pb2.Channel:
    c = channel_pb2.Channel()
    c.name = name
    c.capabilities.groups = groups
    c.capabilities.reactions = reactions
    c.capabilities.edits = edits
    c.capabilities.deletions = deletions
    c.capabilities.read_receipts = read_receipts
    c.capabilities.typing_indicators = typing_indicators
    if supported_content_types:
        c.capabilities.supported_content_types.extend(supported_content_types)
    return c


@pytest.fixture
def mock_ch_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def ns(mock_ch_client: AsyncMock) -> ChannelsNamespace:
    with patch("outbox_sdk.namespaces._channels.ChannelServiceClient") as MockClient:
        MockClient.return_value = mock_ch_client
        return ChannelsNamespace("http://localhost:8080")


@pytest.mark.asyncio
async def test_list_success(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    resp.channels.append(_make_channel("channels/whatsapp"))
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list()

    assert isinstance(result, ListChannelsResult)
    assert len(result.items) == 1
    assert result.items[0].id == "whatsapp"
    assert result.next_page_token is None
    assert result.total_size == 0


@pytest.mark.asyncio
async def test_list_multiple_channels(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    for name in ("channels/whatsapp", "channels/telegram", "channels/signal"):
        resp.channels.append(_make_channel(name))
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list()

    assert len(result.items) == 3
    assert [c.id for c in result.items] == ["whatsapp", "telegram", "signal"]


@pytest.mark.asyncio
async def test_list_empty_response(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list()

    assert result.items == []
    assert result.next_page_token is None
    assert result.total_size == 0


@pytest.mark.asyncio
async def test_list_with_pagination(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    resp.channels.append(_make_channel())
    resp.next_page_token = "tok-xyz"
    resp.total_size = 25
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list(page_size=10, page_token="prev-tok")

    assert result.next_page_token == "tok-xyz"
    assert result.total_size == 25
    req = mock_ch_client.list_channels.call_args[0][0]
    assert req.page_size == 10
    assert req.page_token == "prev-tok"


@pytest.mark.asyncio
async def test_list_empty_next_page_token_is_none(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    resp.next_page_token = ""
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list()

    assert result.next_page_token is None


@pytest.mark.asyncio
async def test_list_default_pagination_params(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    await ns.list()

    req = mock_ch_client.list_channels.call_args[0][0]
    assert req.page_size == 0
    assert req.page_token == ""


@pytest.mark.asyncio
async def test_list_builds_correct_request(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    await ns.list(page_size=25, page_token="abc")

    req = mock_ch_client.list_channels.call_args[0][0]
    assert isinstance(req, channel_pb2.ListChannelsRequest)
    assert req.page_size == 25
    assert req.page_token == "abc"


@pytest.mark.asyncio
async def test_list_channel_with_full_capabilities(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    resp.channels.append(
        _make_channel_with_caps(
            "channels/whatsapp",
            groups=True,
            reactions=True,
            edits=True,
            deletions=True,
            read_receipts=True,
            typing_indicators=True,
            supported_content_types=["text/plain", "image/jpeg", "audio/mpeg"],
        )
    )
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list()

    ch = result.items[0]
    assert isinstance(ch, Channel)
    assert ch.capabilities is not None
    assert isinstance(ch.capabilities, ChannelCapabilities)
    assert ch.capabilities.groups is True
    assert ch.capabilities.reactions is True
    assert ch.capabilities.edits is True
    assert ch.capabilities.deletions is True
    assert ch.capabilities.read_receipts is True
    assert ch.capabilities.typing_indicators is True
    assert ch.capabilities.supported_content_types == ["text/plain", "image/jpeg", "audio/mpeg"]


@pytest.mark.asyncio
async def test_list_channel_with_partial_capabilities(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    resp.channels.append(
        _make_channel_with_caps("channels/signal", read_receipts=True, typing_indicators=True)
    )
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list()

    ch = result.items[0]
    assert ch.capabilities is not None
    assert ch.capabilities.groups is False
    assert ch.capabilities.reactions is False
    assert ch.capabilities.read_receipts is True
    assert ch.capabilities.typing_indicators is True


@pytest.mark.asyncio
async def test_list_channel_without_capabilities(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    resp.channels.append(_make_channel("channels/telegram"))
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list()

    assert result.items[0].capabilities is None


@pytest.mark.asyncio
async def test_list_channel_empty_supported_content_types(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    c = channel_pb2.Channel()
    c.name = "channels/whatsapp"
    c.capabilities.read_receipts = True
    resp.channels.append(c)
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list()

    assert result.items[0].capabilities is not None
    assert result.items[0].capabilities.supported_content_types == []


@pytest.mark.asyncio
async def test_list_channel_with_create_time(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    c = channel_pb2.Channel()
    c.name = "channels/whatsapp"
    ts = Timestamp()
    ts.seconds = 1700000000
    c.create_time.CopyFrom(ts)
    resp.channels.append(c)
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list()

    assert result.items[0].create_time is not None
    assert result.items[0].create_time.year == 2023


@pytest.mark.asyncio
async def test_list_channel_without_create_time(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    resp.channels.append(_make_channel())
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    assert (await ns.list()).items[0].create_time is None


@pytest.mark.asyncio
async def test_list_items_are_channel_type(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    resp.channels.append(_make_channel("channels/ch1"))
    resp.channels.append(_make_channel("channels/ch2"))
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list()

    assert all(isinstance(item, Channel) for item in result.items)


@pytest.mark.asyncio
async def test_list_result_repr(ns: ChannelsNamespace, mock_ch_client: AsyncMock) -> None:
    resp = channel_pb2.ListChannelsResponse()
    resp.channels.append(_make_channel())
    resp.next_page_token = "tok"
    resp.total_size = 1
    mock_ch_client.list_channels = AsyncMock(return_value=resp)

    result = await ns.list()

    repr_str = repr(result)
    assert "ListChannelsResult" in repr_str
    assert "items=" in repr_str
    assert "next_page_token=" in repr_str
    assert "total_size=" in repr_str


def test_namespace_initialization() -> None:
    mock_client = AsyncMock()
    with patch("outbox_sdk.namespaces._channels.ChannelServiceClient") as MockClient:
        MockClient.return_value = mock_client
        ChannelsNamespace("https://api.example.com")
    MockClient.assert_called_once_with("https://api.example.com", interceptors=())


def test_namespace_initialization_with_interceptors() -> None:
    mock_client = AsyncMock()
    mock_interceptor = AsyncMock()
    with patch("outbox_sdk.namespaces._channels.ChannelServiceClient") as MockClient:
        MockClient.return_value = mock_client
        ChannelsNamespace("https://api.example.com", interceptors=(mock_interceptor,))
    MockClient.assert_called_once_with("https://api.example.com", interceptors=(mock_interceptor,))
