"""Tests for OutboxClient async context manager."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from outbox_sdk import OutboxClient


@pytest.mark.asyncio
async def test_context_manager_closes_all_namespaces() -> None:
    """__aexit__ must call close() on every namespace."""
    mock_ns = AsyncMock()

    with (
        patch("outbox_sdk.AccountsNamespace", return_value=mock_ns),
        patch("outbox_sdk.ChannelsNamespace", return_value=mock_ns),
        patch("outbox_sdk.ConnectorsNamespace", return_value=mock_ns),
        patch("outbox_sdk.DestinationsNamespace", return_value=mock_ns),
        patch("outbox_sdk.MessagesNamespace", return_value=mock_ns),
    ):
        async with OutboxClient(api_key="test-key"):
            pass

    # close() is called once per namespace (5 namespaces share the same mock here)
    assert mock_ns.close.await_count == 5


@pytest.mark.asyncio
async def test_context_manager_returns_self() -> None:
    """__aenter__ returns the OutboxClient instance."""
    mock_ns = AsyncMock()

    with (
        patch("outbox_sdk.AccountsNamespace", return_value=mock_ns),
        patch("outbox_sdk.ChannelsNamespace", return_value=mock_ns),
        patch("outbox_sdk.ConnectorsNamespace", return_value=mock_ns),
        patch("outbox_sdk.DestinationsNamespace", return_value=mock_ns),
        patch("outbox_sdk.MessagesNamespace", return_value=mock_ns),
    ):
        client = OutboxClient(api_key="test-key")
        async with client as ctx:
            assert ctx is client
