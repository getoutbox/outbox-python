"""Tests for DestinationsNamespace using mocked gRPC clients."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from outbox.v1 import destination_pb2
from outbox_sdk._enums import DestinationEventType, DestinationPayloadFormat, DestinationState
from outbox_sdk._types import Destination, DestinationTestResult
from outbox_sdk.namespaces._destinations import DestinationsNamespace, ListDestinationsResult


def _make_destination(
    name: str = "destinations/dest-1",
    display_name: str = "Test Dest",
    state: destination_pb2.Destination.State = destination_pb2.Destination.State.STATE_ACTIVE,
) -> destination_pb2.Destination:
    d = destination_pb2.Destination()
    d.name = name
    d.display_name = display_name
    d.state = state
    d.webhook.url = "https://example.com/hook"
    return d


@pytest.fixture
def mock_dest_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def ns(mock_dest_client: AsyncMock) -> DestinationsNamespace:
    with patch("outbox_sdk.namespaces._destinations.DestinationServiceClient") as MockClient:
        MockClient.return_value = mock_dest_client
        return DestinationsNamespace("http://localhost:8080")


@pytest.mark.asyncio
async def test_create_success(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.CreateDestinationResponse()
    resp.destination.CopyFrom(_make_destination())
    mock_dest_client.create_destination = AsyncMock(return_value=resp)

    result = await ns.create(
        target_type="webhook",
        display_name="Test Dest",
        target_config={"url": "https://example.com/hook"},
    )

    assert isinstance(result, Destination)
    assert result.id == "dest-1"
    assert result.display_name == "Test Dest"
    assert result.state == DestinationState.ACTIVE


@pytest.mark.asyncio
async def test_create_builds_correct_proto(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.CreateDestinationResponse()
    resp.destination.CopyFrom(_make_destination())
    mock_dest_client.create_destination = AsyncMock(return_value=resp)

    await ns.create(
        target_type="webhook",
        display_name="My Hook",
        target_config={"url": "https://example.com/hook", "signing_secret": "s3cr3t"},
        event_types=[DestinationEventType.MESSAGE, DestinationEventType.DELIVERY_UPDATE],
        filter_='connector == "connectors/abc"',
        payload_format=DestinationPayloadFormat.JSON,
        destination_id="dest-custom",
        request_id="req-1",
    )

    req = mock_dest_client.create_destination.call_args[0][0]
    assert req.destination.display_name == "My Hook"
    assert req.destination.webhook.url == "https://example.com/hook"
    assert req.destination.webhook.signing_secret == "s3cr3t"
    assert req.destination.filter == 'connector == "connectors/abc"'  # maps from filter_
    assert req.destination_id == "dest-custom"
    assert req.request_id == "req-1"
    assert req.destination.payload_format == int(DestinationPayloadFormat.JSON)
    event_types = list(req.destination.event_types)
    assert destination_pb2.Destination.EVENT_TYPE_MESSAGE in event_types
    assert destination_pb2.Destination.EVENT_TYPE_DELIVERY_UPDATE in event_types


@pytest.mark.asyncio
async def test_create_empty_response_raises(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.CreateDestinationResponse()
    mock_dest_client.create_destination = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty destination"):
        await ns.create(target_type="webhook")


@pytest.mark.asyncio
async def test_get_success(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.GetDestinationResponse()
    resp.destination.CopyFrom(_make_destination())
    mock_dest_client.get_destination = AsyncMock(return_value=resp)

    result = await ns.get("dest-1")

    assert result.id == "dest-1"
    req = mock_dest_client.get_destination.call_args[0][0]
    assert req.name == "destinations/dest-1"


@pytest.mark.asyncio
async def test_get_empty_response_raises(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.GetDestinationResponse()
    mock_dest_client.get_destination = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty destination"):
        await ns.get("dest-1")


@pytest.mark.asyncio
async def test_list_pagination(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.ListDestinationsResponse()
    resp.destinations.append(_make_destination("destinations/dest-1"))
    resp.destinations.append(_make_destination("destinations/dest-2"))
    resp.next_page_token = "tok-xyz"
    resp.total_size = 7
    mock_dest_client.list_destinations = AsyncMock(return_value=resp)

    result = await ns.list(page_size=2, page_token="prev")

    assert isinstance(result, ListDestinationsResult)
    assert len(result.items) == 2
    assert result.items[0].id == "dest-1"
    assert result.next_page_token == "tok-xyz"
    assert result.total_size == 7

    req = mock_dest_client.list_destinations.call_args[0][0]
    assert req.page_size == 2
    assert req.page_token == "prev"


@pytest.mark.asyncio
async def test_list_empty_next_page_token(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.ListDestinationsResponse()
    resp.next_page_token = ""
    mock_dest_client.list_destinations = AsyncMock(return_value=resp)

    result = await ns.list()

    assert result.next_page_token is None


@pytest.mark.asyncio
async def test_list_with_filter(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.ListDestinationsResponse()
    mock_dest_client.list_destinations = AsyncMock(return_value=resp)

    await ns.list(filter_='state == "active"', order_by="create_time desc")

    req = mock_dest_client.list_destinations.call_args[0][0]
    assert req.filter == 'state == "active"'
    assert req.order_by == "create_time desc"


@pytest.mark.asyncio
async def test_update_display_name(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.UpdateDestinationResponse()
    d = _make_destination()
    d.display_name = "Updated"
    resp.destination.CopyFrom(d)
    mock_dest_client.update_destination = AsyncMock(return_value=resp)

    result = await ns.update(id_="dest-1", display_name="Updated")

    assert result.display_name == "Updated"
    req = mock_dest_client.update_destination.call_args[0][0]
    assert req.destination.name == "destinations/dest-1"
    assert req.destination.display_name == "Updated"
    assert "display_name" in list(req.update_mask.paths)


@pytest.mark.asyncio
async def test_update_event_types(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.UpdateDestinationResponse()
    d = _make_destination()
    d.event_types.append(destination_pb2.Destination.EVENT_TYPE_MESSAGE)
    resp.destination.CopyFrom(d)
    mock_dest_client.update_destination = AsyncMock(return_value=resp)

    await ns.update(id_="dest-1", event_types=[DestinationEventType.MESSAGE])

    req = mock_dest_client.update_destination.call_args[0][0]
    assert "event_types" in list(req.update_mask.paths)
    assert destination_pb2.Destination.EVENT_TYPE_MESSAGE in list(req.destination.event_types)


@pytest.mark.asyncio
async def test_update_filter_expression(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.UpdateDestinationResponse()
    d = _make_destination()
    d.filter = 'connector == "connectors/xyz"'
    resp.destination.CopyFrom(d)
    mock_dest_client.update_destination = AsyncMock(return_value=resp)

    await ns.update(id_="dest-1", filter_='connector == "connectors/xyz"')

    req = mock_dest_client.update_destination.call_args[0][0]
    assert req.destination.filter == 'connector == "connectors/xyz"'
    assert "filter" in list(req.update_mask.paths)


@pytest.mark.asyncio
async def test_update_target_config(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.UpdateDestinationResponse()
    resp.destination.CopyFrom(_make_destination())
    mock_dest_client.update_destination = AsyncMock(return_value=resp)

    await ns.update(
        id_="dest-1",
        target_type="webhook",
        target_config={"url": "https://new.example.com/hook"},
    )

    req = mock_dest_client.update_destination.call_args[0][0]
    assert req.destination.webhook.url == "https://new.example.com/hook"
    assert "webhook" in list(req.update_mask.paths)


@pytest.mark.asyncio
async def test_update_empty_response_raises(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.UpdateDestinationResponse()
    mock_dest_client.update_destination = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty destination"):
        await ns.update(id_="dest-1", display_name="x")


@pytest.mark.asyncio
async def test_delete(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.DeleteDestinationResponse()
    mock_dest_client.delete_destination = AsyncMock(return_value=resp)

    await ns.delete("dest-1")

    req = mock_dest_client.delete_destination.call_args[0][0]
    assert req.name == "destinations/dest-1"


@pytest.mark.asyncio
async def test_test_success(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.TestDestinationResponse()
    resp.success = True
    mock_dest_client.test_destination = AsyncMock(return_value=resp)

    result = await ns.test("dest-1")

    assert isinstance(result, DestinationTestResult)
    assert result.success is True
    assert result.error_message == ""

    req = mock_dest_client.test_destination.call_args[0][0]
    assert req.name == "destinations/dest-1"


@pytest.mark.asyncio
async def test_test_failure_with_message(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.TestDestinationResponse()
    resp.success = False
    resp.error_message = "connection refused"
    mock_dest_client.test_destination = AsyncMock(return_value=resp)

    result = await ns.test("dest-1")

    assert result.success is False
    assert result.error_message == "connection refused"


@pytest.mark.asyncio
async def test_create_webhook_with_headers(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    resp = destination_pb2.CreateDestinationResponse()
    d = destination_pb2.Destination()
    d.name = "destinations/dest-1"
    d.webhook.url = "https://example.com/hook"
    d.webhook.headers["X-Auth"] = "token-abc"
    resp.destination.CopyFrom(d)
    mock_dest_client.create_destination = AsyncMock(return_value=resp)

    await ns.create(
        target_type="webhook",
        target_config={"url": "https://example.com/hook", "headers": {"X-Auth": "token-abc"}},
    )

    req = mock_dest_client.create_destination.call_args[0][0]
    assert req.destination.webhook.headers["X-Auth"] == "token-abc"


@pytest.mark.asyncio
async def test_create_invalid_target_type_raises(
    ns: DestinationsNamespace, mock_dest_client: AsyncMock
) -> None:
    with pytest.raises(ValueError, match="Invalid target_type"):
        await ns.create(
            target_type="not_a_real_target",  # type: ignore[arg-type]
            target_config={"url": "https://example.com"},
        )


@pytest.mark.asyncio
async def test_update_invalid_target_type_raises(
    ns: DestinationsNamespace, mock_dest_client: AsyncMock
) -> None:
    with pytest.raises(ValueError, match="Invalid target_type"):
        await ns.update(
            id_="dest-1",
            target_type="not_a_real_target",  # type: ignore[arg-type]
            target_config={"url": "https://example.com"},
        )


@pytest.mark.asyncio
async def test_list_returns_destination_with_target_type(
    ns: DestinationsNamespace, mock_dest_client: AsyncMock
) -> None:
    resp = destination_pb2.ListDestinationsResponse()
    d = destination_pb2.Destination()
    d.name = "destinations/dest-webhook"
    d.display_name = "Webhook Destination"
    d.state = destination_pb2.Destination.State.STATE_ACTIVE
    d.webhook.url = "https://example.com/hook"
    resp.destinations.append(d)
    resp.total_size = 1
    mock_dest_client.list_destinations = AsyncMock(return_value=resp)

    result = await ns.list()

    assert len(result.items) == 1
    item = result.items[0]
    assert item.id == "dest-webhook"
    assert item.display_name == "Webhook Destination"
    assert item.target_type == "webhook"
    assert item.target_config is not None
    assert item.target_config["url"] == "https://example.com/hook"


class _StopPollingError(Exception):
    """Sentinel used in tests to break out of listen's infinite loop."""


def _make_proto_delivery_event(delivery_id: str = "del-1") -> destination_pb2.DeliveryEvent:
    evt = destination_pb2.DeliveryEvent()
    evt.delivery_id = delivery_id
    evt.destination = "destinations/dest-1"
    evt.connector = "connectors/conn-1"
    return evt


def _make_poll_response(
    events: list[destination_pb2.DeliveryEvent], cursor: str = ""
) -> destination_pb2.PollEventsResponse:
    resp = destination_pb2.PollEventsResponse()
    resp.events.extend(events)
    resp.cursor = cursor
    return resp


@pytest.mark.asyncio
async def test_listen_yields_events(ns: DestinationsNamespace, mock_dest_client: AsyncMock) -> None:
    evt = _make_proto_delivery_event("del-1")
    # First call returns one event; second call raises _StopPollingError to break
    # out of the infinite loop in the test.
    call_count = 0

    async def side_effect(req: object) -> destination_pb2.PollEventsResponse:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return _make_poll_response([evt], cursor="cur-1")
        raise _StopPollingError

    mock_dest_client.poll_events = AsyncMock(side_effect=side_effect)

    events: list[object] = []

    async def _run() -> None:
        async for event in ns.listen("dest-1"):
            events.append(event)  # noqa: PERF401

    with pytest.raises(_StopPollingError):
        await _run()

    assert len(events) == 1


@pytest.mark.asyncio
async def test_listen_passes_cursor_to_next_request(
    ns: DestinationsNamespace, mock_dest_client: AsyncMock
) -> None:
    evt = _make_proto_delivery_event()
    call_count = 0

    async def side_effect(req: destination_pb2.PollEventsRequest) -> destination_pb2.PollEventsResponse:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return _make_poll_response([evt], cursor="cur-abc")
        raise _StopPollingError

    mock_dest_client.poll_events = AsyncMock(side_effect=side_effect)

    with pytest.raises(_StopPollingError):
        async for _ in ns.listen("dest-1"):
            pass

    second_req = mock_dest_client.poll_events.call_args_list[1][0][0]
    assert second_req.cursor == "cur-abc"


@pytest.mark.asyncio
async def test_listen_uses_resume_cursor_as_initial_cursor(
    ns: DestinationsNamespace, mock_dest_client: AsyncMock
) -> None:
    async def side_effect(req: destination_pb2.PollEventsRequest) -> destination_pb2.PollEventsResponse:
        raise _StopPollingError

    mock_dest_client.poll_events = AsyncMock(side_effect=side_effect)

    with pytest.raises(_StopPollingError):
        async for _ in ns.listen("dest-1", resume_cursor="saved-cursor"):
            pass

    first_req = mock_dest_client.poll_events.call_args_list[0][0][0]
    assert first_req.cursor == "saved-cursor"
    assert first_req.name == "destinations/dest-1"


@pytest.mark.asyncio
async def test_listen_empty_response_loops_back(
    ns: DestinationsNamespace, mock_dest_client: AsyncMock
) -> None:
    call_count = 0

    async def side_effect(req: destination_pb2.PollEventsRequest) -> destination_pb2.PollEventsResponse:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return _make_poll_response([], cursor="cur-loop")
        raise _StopPollingError

    mock_dest_client.poll_events = AsyncMock(side_effect=side_effect)

    with pytest.raises(_StopPollingError):
        async for _ in ns.listen("dest-1"):
            pass

    assert mock_dest_client.poll_events.call_count == 3


@pytest.mark.asyncio
async def test_listen_forwards_max_events_and_wait_seconds(
    ns: DestinationsNamespace, mock_dest_client: AsyncMock
) -> None:
    async def side_effect(req: destination_pb2.PollEventsRequest) -> destination_pb2.PollEventsResponse:
        raise _StopPollingError

    mock_dest_client.poll_events = AsyncMock(side_effect=side_effect)

    with pytest.raises(_StopPollingError):
        async for _ in ns.listen("dest-1", max_events=5, wait_seconds=20):
            pass

    first_req = mock_dest_client.poll_events.call_args_list[0][0][0]
    assert first_req.max_events == 5
    assert first_req.wait_seconds == 20
