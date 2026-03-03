# packages/sdk/src/outbox_sdk/namespaces/_channels.py
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from outbox.v1.channel_connect import ChannelServiceClient
from outbox.v1.channel_pb2 import GetChannelRequest, ListChannelsRequest
from outbox_sdk._mappers import map_channel

if TYPE_CHECKING:
    from connectrpc.interceptor import Interceptor
    from outbox_sdk._types import Channel


@dataclass
class ListChannelsResult:
    items: list[Channel]
    next_page_token: str | None
    total_size: int


class ChannelsNamespace:
    def __init__(self, base_url: str, interceptors: tuple[Interceptor, ...] = ()) -> None:  # type: ignore[reportUnknownParameterType]
        self._client = ChannelServiceClient(base_url, interceptors=interceptors)

    async def close(self) -> None:
        await self._client.close()

    async def get(self, id_: str) -> Channel:
        req = GetChannelRequest(name=f"channels/{id_}")
        res = await self._client.get_channel(req)
        return map_channel(res.channel)

    async def list(
        self,
        *,
        page_size: int = 0,
        page_token: str = "",
    ) -> ListChannelsResult:
        req = ListChannelsRequest(page_size=page_size, page_token=page_token)
        res = await self._client.list_channels(req)
        return ListChannelsResult(
            items=[map_channel(c) for c in res.channels],
            next_page_token=res.next_page_token or None,
            total_size=res.total_size,
        )
