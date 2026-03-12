# packages/sdk/src/outbox_sdk/namespaces/_destinations.py
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from google.protobuf.field_mask_pb2 import FieldMask
from outbox.v1.destination_connect import DestinationServiceClient
from outbox.v1.destination_pb2 import (
    CreateDestinationRequest,
    DeleteDestinationRequest,
    GetDestinationRequest,
    ListDestinationsRequest,
    ListDestinationTestResultsRequest,
    PollEventsRequest,
    TestDestinationRequest,
    UpdateDestinationRequest,
    ValidateDestinationFilterRequest,
)
from outbox.v1.destination_pb2 import (
    Destination as ProtoDestination,
)
from outbox_sdk._enums import DestinationEventType, DestinationPayloadFormat
from outbox_sdk._field_mask import derive_field_mask
from outbox_sdk._mappers import map_delivery_event, map_destination, proto_ts
from outbox_sdk._resource_names import destination_name
from outbox_sdk._types import (
    DestinationTargetType,
    DestinationTestResult,
    DestinationTestResultItem,
    ValidateFilterResult,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, AsyncIterator

    from connectrpc.interceptor import Interceptor
    from outbox_sdk._types import DeliveryEvent, Destination

_VALID_TARGET_TYPES: frozenset[str] = frozenset(
    DestinationTargetType.__args__  # type: ignore[attr-defined]
)


@dataclass
class ListDestinationsResult:
    items: list[Destination]
    next_page_token: str | None
    total_size: int


class DestinationsNamespace:
    def __init__(self, base_url: str, interceptors: tuple[Interceptor, ...] = ()) -> None:  # type: ignore[reportUnknownParameterType]
        self._client = DestinationServiceClient(base_url, interceptors=interceptors)

    async def close(self) -> None:
        await self._client.close()

    async def create(
        self,
        *,
        target_type: DestinationTargetType,
        display_name: str = "",
        target_config: dict[str, object] | None = None,
        event_types: list[DestinationEventType] | None = None,
        filter_: str = "",
        payload_format: DestinationPayloadFormat = DestinationPayloadFormat.UNSPECIFIED,
        destination_id: str = "",
        request_id: str = "",
    ) -> Destination:
        if target_type not in _VALID_TARGET_TYPES:
            msg = f"Invalid target_type: {target_type!r}"
            raise ValueError(msg)
        dest = ProtoDestination(
            display_name=display_name,
            filter=filter_,
            payload_format=cast("ProtoDestination.PayloadFormat", payload_format),
        )
        if event_types:
            dest.event_types.extend(cast("ProtoDestination.EventType", e) for e in event_types)

        if target_config:
            target_msg = getattr(dest, target_type, None)
            if target_msg is not None:
                for k, v in target_config.items():
                    if hasattr(v, "items"):
                        getattr(target_msg, k).update(v)
                    elif hasattr(v, "__iter__") and not isinstance(v, (str, bytes)):
                        getattr(target_msg, k).extend(v)
                    else:
                        setattr(target_msg, k, v)

        req = CreateDestinationRequest(
            destination=dest,
            destination_id=destination_id,
            request_id=request_id,
        )
        res = await self._client.create_destination(req)
        if not res.HasField("destination"):
            msg = "create_destination: server returned empty destination"
            raise RuntimeError(msg)
        return map_destination(res.destination)

    async def get(self, id_: str) -> Destination:
        req = GetDestinationRequest(name=destination_name(id_))
        res = await self._client.get_destination(req)
        if not res.HasField("destination"):
            msg = "get_destination: server returned empty destination"
            raise RuntimeError(msg)
        return map_destination(res.destination)

    async def list(
        self,
        *,
        filter_: str = "",
        order_by: str = "",
        page_size: int = 0,
        page_token: str = "",
    ) -> ListDestinationsResult:
        req = ListDestinationsRequest(
            filter=filter_,
            order_by=order_by,
            page_size=page_size,
            page_token=page_token,
        )
        res = await self._client.list_destinations(req)
        return ListDestinationsResult(
            items=[map_destination(d) for d in res.destinations],
            next_page_token=res.next_page_token or None,
            total_size=res.total_size,
        )

    async def update(  # noqa: C901
        self,
        *,
        id_: str,
        display_name: str | None = None,
        event_types: list[DestinationEventType] | None = None,
        filter_: str | None = None,
        payload_format: DestinationPayloadFormat | None = None,
        target_type: DestinationTargetType | None = None,
        target_config: dict[str, object] | None = None,
    ) -> Destination:
        fields: dict[str, object] = {
            "display_name": display_name,
            "event_types": event_types,
            "filter": filter_,
            "payload_format": payload_format,
        }
        dest = ProtoDestination(name=destination_name(id_))
        if display_name is not None:
            dest.display_name = display_name
        if event_types is not None:
            dest.event_types.extend(cast("ProtoDestination.EventType", e) for e in event_types)
        if filter_ is not None:
            dest.filter = filter_
        if payload_format is not None:
            dest.payload_format = cast("ProtoDestination.PayloadFormat", payload_format)
        if target_type is not None and target_type not in _VALID_TARGET_TYPES:
            msg = f"Invalid target_type: {target_type!r}"
            raise ValueError(msg)
        if target_type and target_config:
            fields[target_type] = target_config
            target_msg = getattr(dest, target_type, None)
            if target_msg is not None:
                for k, v in target_config.items():
                    if hasattr(v, "items"):
                        getattr(target_msg, k).update(v)
                    elif hasattr(v, "__iter__") and not isinstance(v, (str, bytes)):
                        getattr(target_msg, k).extend(v)
                    else:
                        setattr(target_msg, k, v)

        req = UpdateDestinationRequest(
            destination=dest,
            update_mask=FieldMask(paths=derive_field_mask(fields)),
        )
        res = await self._client.update_destination(req)
        if not res.HasField("destination"):
            msg = "update_destination: server returned empty destination"
            raise RuntimeError(msg)
        return map_destination(res.destination)

    async def delete(self, id_: str) -> None:
        req = DeleteDestinationRequest(name=destination_name(id_))
        await self._client.delete_destination(req)

    async def test(self, id_: str) -> DestinationTestResult:
        req = TestDestinationRequest(name=destination_name(id_))
        res = await self._client.test_destination(req)
        return DestinationTestResult(
            success=res.success,
            error_message=res.error_message,
            http_status_code=res.http_status_code,
            latency_ms=res.latency_ms,
        )

    async def list_test_results(self, id_: str, *, page_size: int = 0) -> list[DestinationTestResultItem]:
        req = ListDestinationTestResultsRequest(name=destination_name(id_), page_size=page_size)
        res = await self._client.list_destination_test_results(req)
        return [
            DestinationTestResultItem(
                success=r.success,
                error_message=r.error_message,
                http_status_code=r.http_status_code,
                latency_ms=r.latency_ms,
                test_time=proto_ts(r.test_time),
            )
            for r in res.results
        ]

    async def validate_filter(self, filter_: str, *, sample_size: int = 0) -> ValidateFilterResult:
        req = ValidateDestinationFilterRequest(filter=filter_, sample_size=sample_size)
        res = await self._client.validate_destination_filter(req)
        return ValidateFilterResult(
            valid=res.valid,
            error_message=res.error_message,
            matched_count=res.matched_count,
            total_count=res.total_count,
        )

    async def listen(
        self,
        id_: str,
        *,
        resume_cursor: str = "",
        max_events: int = 0,
        wait_seconds: int = 0,
    ) -> AsyncGenerator[DeliveryEvent, None]:
        """Listen for events from a local destination using long polling.

        Yields DeliveryEvent instances as they arrive. Runs until the
        caller stops iterating or an error occurs.

        Pass resume_cursor to resume from a known position after restart.
        """
        cursor = resume_cursor
        while True:
            req = PollEventsRequest(
                name=destination_name(id_),
                cursor=cursor,
                max_events=max_events,
                wait_seconds=wait_seconds,
            )
            res = await self._client.poll_events(req)
            cursor = res.cursor
            for event in res.events:
                yield map_delivery_event(event)
