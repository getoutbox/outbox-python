"""Tests for AccountsNamespace using mocked gRPC clients."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from outbox.v1 import account_pb2
from outbox_sdk._enums import AccountSource
from outbox_sdk._types import Account
from outbox_sdk.namespaces._accounts import AccountsNamespace, ListAccountsResult


def _make_account(
    name: str = "accounts/acc-1",
    contact_id: str = "contact-1",
    external_id: str = "ext-1",
) -> account_pb2.Account:
    a = account_pb2.Account()
    a.name = name
    a.contact_id = contact_id
    a.external_id = external_id
    a.source = account_pb2.Account.SOURCE_API
    return a


@pytest.fixture
def mock_acc_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def ns(mock_acc_client: AsyncMock) -> AccountsNamespace:
    with patch("outbox_sdk.namespaces._accounts.AccountServiceClient") as MockClient:
        MockClient.return_value = mock_acc_client
        return AccountsNamespace("http://localhost:8080")


@pytest.mark.asyncio
async def test_create_success(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.CreateAccountResponse()
    resp.account.CopyFrom(_make_account())
    mock_acc_client.create_account = AsyncMock(return_value=resp)

    result = await ns.create(contact_id="contact-1", external_id="ext-1")

    assert isinstance(result, Account)
    assert result.id == "acc-1"
    assert result.contact_id == "contact-1"
    assert result.external_id == "ext-1"
    assert result.source == AccountSource.API


@pytest.mark.asyncio
async def test_create_with_metadata(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.CreateAccountResponse()
    a = _make_account()
    a.metadata["key"] = "value"
    resp.account.CopyFrom(a)
    mock_acc_client.create_account = AsyncMock(return_value=resp)

    await ns.create(contact_id="c", external_id="e", metadata={"key": "value"})

    req = mock_acc_client.create_account.call_args[0][0]
    assert req.account.metadata["key"] == "value"


@pytest.mark.asyncio
async def test_create_builds_correct_proto(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.CreateAccountResponse()
    resp.account.CopyFrom(_make_account())
    mock_acc_client.create_account = AsyncMock(return_value=resp)

    await ns.create(contact_id="contact-1", external_id="ext-1", request_id="req-abc")

    req = mock_acc_client.create_account.call_args[0][0]
    assert req.account.contact_id == "contact-1"
    assert req.account.external_id == "ext-1"
    assert req.request_id == "req-abc"


@pytest.mark.asyncio
async def test_create_empty_response_raises(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.CreateAccountResponse()
    mock_acc_client.create_account = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty account"):
        await ns.create(contact_id="c", external_id="e")


@pytest.mark.asyncio
async def test_get_success(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.GetAccountResponse()
    resp.account.CopyFrom(_make_account())
    mock_acc_client.get_account = AsyncMock(return_value=resp)

    result = await ns.get("acc-1")

    assert result.id == "acc-1"
    req = mock_acc_client.get_account.call_args[0][0]
    assert req.name == "accounts/acc-1"


@pytest.mark.asyncio
async def test_get_empty_response_raises(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.GetAccountResponse()
    mock_acc_client.get_account = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty account"):
        await ns.get("acc-1")


@pytest.mark.asyncio
async def test_list_pagination(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.ListAccountsResponse()
    resp.accounts.append(_make_account("accounts/acc-1"))
    resp.accounts.append(_make_account("accounts/acc-2"))
    resp.next_page_token = "tok-abc"
    resp.total_size = 10
    mock_acc_client.list_accounts = AsyncMock(return_value=resp)

    result = await ns.list(page_size=2, page_token="prev-tok")

    assert isinstance(result, ListAccountsResult)
    assert len(result.items) == 2
    assert result.items[0].id == "acc-1"
    assert result.items[1].id == "acc-2"
    assert result.next_page_token == "tok-abc"
    assert result.total_size == 10

    req = mock_acc_client.list_accounts.call_args[0][0]
    assert req.page_size == 2
    assert req.page_token == "prev-tok"


@pytest.mark.asyncio
async def test_list_empty_next_page_token(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.ListAccountsResponse()
    resp.next_page_token = ""
    mock_acc_client.list_accounts = AsyncMock(return_value=resp)

    result = await ns.list()

    assert result.next_page_token is None


@pytest.mark.asyncio
async def test_list_with_filter(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.ListAccountsResponse()
    mock_acc_client.list_accounts = AsyncMock(return_value=resp)

    await ns.list(filter_='external_id == "ext-1"', order_by="create_time desc")

    req = mock_acc_client.list_accounts.call_args[0][0]
    assert req.filter == 'external_id == "ext-1"'
    assert req.order_by == "create_time desc"


@pytest.mark.asyncio
async def test_update_metadata(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.UpdateAccountResponse()
    a = _make_account()
    a.metadata["k"] = "v"
    resp.account.CopyFrom(a)
    mock_acc_client.update_account = AsyncMock(return_value=resp)

    result = await ns.update(id_="acc-1", metadata={"k": "v"})

    assert result.id == "acc-1"
    assert result.metadata == {"k": "v"}

    req = mock_acc_client.update_account.call_args[0][0]
    assert req.account.name == "accounts/acc-1"
    assert req.account.metadata["k"] == "v"
    assert "metadata" in list(req.update_mask.paths)


@pytest.mark.asyncio
async def test_update_empty_response_raises(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.UpdateAccountResponse()
    mock_acc_client.update_account = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty account"):
        await ns.update(id_="acc-1", metadata={"k": "v"})


@pytest.mark.asyncio
async def test_delete(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.DeleteAccountResponse()
    mock_acc_client.delete_account = AsyncMock(return_value=resp)

    await ns.delete("acc-1")

    req = mock_acc_client.delete_account.call_args[0][0]
    assert req.name == "accounts/acc-1"


@pytest.mark.asyncio
async def test_resolve_success(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.ResolveAccountResponse()
    resp.account.CopyFrom(_make_account(external_id="ext-xyz"))
    mock_acc_client.resolve_account = AsyncMock(return_value=resp)

    result = await ns.resolve(external_id="ext-xyz")

    assert result.external_id == "ext-xyz"
    req = mock_acc_client.resolve_account.call_args[0][0]
    assert req.external_id == "ext-xyz"


@pytest.mark.asyncio
async def test_resolve_empty_response_raises(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.ResolveAccountResponse()
    mock_acc_client.resolve_account = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty account"):
        await ns.resolve(external_id="ext-1")


@pytest.mark.asyncio
async def test_claim_success(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.ClaimAccountResponse()
    a = _make_account()
    a.contact_id = "new-contact"
    resp.account.CopyFrom(a)
    mock_acc_client.claim_account = AsyncMock(return_value=resp)

    result = await ns.claim(id_="acc-1", contact_id="new-contact")

    assert result.contact_id == "new-contact"
    req = mock_acc_client.claim_account.call_args[0][0]
    assert req.name == "accounts/acc-1"
    assert req.contact_id == "new-contact"


@pytest.mark.asyncio
async def test_claim_with_request_id(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.ClaimAccountResponse()
    resp.account.CopyFrom(_make_account())
    mock_acc_client.claim_account = AsyncMock(return_value=resp)

    await ns.claim(id_="acc-1", contact_id="c", request_id="req-123")

    req = mock_acc_client.claim_account.call_args[0][0]
    assert req.request_id == "req-123"


@pytest.mark.asyncio
async def test_claim_empty_response_raises(ns: AccountsNamespace, mock_acc_client: AsyncMock) -> None:
    resp = account_pb2.ClaimAccountResponse()
    mock_acc_client.claim_account = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty account"):
        await ns.claim(id_="acc-1", contact_id="c")
