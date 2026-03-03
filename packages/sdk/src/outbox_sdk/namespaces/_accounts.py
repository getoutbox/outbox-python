# packages/sdk/src/outbox_sdk/namespaces/_accounts.py
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from google.protobuf.field_mask_pb2 import FieldMask
from outbox.v1.account_connect import AccountServiceClient
from outbox.v1.account_pb2 import (
    Account as ProtoAccount,
)
from outbox.v1.account_pb2 import (
    ClaimAccountRequest,
    CreateAccountRequest,
    DeleteAccountRequest,
    GetAccountRequest,
    ListAccountsRequest,
    ResolveAccountRequest,
    UpdateAccountRequest,
)

from outbox_sdk._field_mask import derive_field_mask
from outbox_sdk._mappers import map_account
from outbox_sdk._resource_names import account_name

if TYPE_CHECKING:
    from outbox_sdk._types import Account
    from outbox_sdk.namespaces import Interceptors


@dataclass
class ListAccountsResult:
    items: list[Account]
    next_page_token: str | None
    total_size: int


class AccountsNamespace:
    def __init__(self, base_url: str, interceptors: Interceptors = ()) -> None:
        self._client = AccountServiceClient(base_url, interceptors=interceptors)

    async def close(self) -> None:
        await self._client.close()

    async def create(
        self,
        *,
        contact_id: str,
        external_id: str,
        metadata: dict[str, str] | None = None,
        request_id: str = "",
    ) -> Account:
        account = ProtoAccount(
            contact_id=contact_id,
            external_id=external_id,
        )
        if metadata is not None:
            account.metadata.update(metadata)

        req = CreateAccountRequest(account=account, request_id=request_id)
        res = await self._client.create_account(req)
        if not res.HasField("account"):
            msg = "create_account: server returned empty account"
            raise RuntimeError(msg)
        return map_account(res.account)

    async def get(self, id_: str) -> Account:
        req = GetAccountRequest(name=account_name(id_))
        res = await self._client.get_account(req)
        if not res.HasField("account"):
            msg = "get_account: server returned empty account"
            raise RuntimeError(msg)
        return map_account(res.account)

    async def list(
        self,
        *,
        filter_: str = "",
        order_by: str = "",
        page_size: int = 0,
        page_token: str = "",
    ) -> ListAccountsResult:
        req = ListAccountsRequest(
            filter=filter_,
            order_by=order_by,
            page_size=page_size,
            page_token=page_token,
        )
        res = await self._client.list_accounts(req)
        return ListAccountsResult(
            items=[map_account(i) for i in res.accounts],
            next_page_token=res.next_page_token or None,
            total_size=res.total_size,
        )

    async def update(
        self,
        *,
        id_: str,
        metadata: dict[str, str] | None = None,
    ) -> Account:
        fields: dict[str, object] = {"metadata": metadata}
        account = ProtoAccount(name=account_name(id_))
        if metadata is not None:
            account.metadata.update(metadata)

        req = UpdateAccountRequest(
            account=account,
            update_mask=FieldMask(paths=derive_field_mask(fields)),
        )
        res = await self._client.update_account(req)
        if not res.HasField("account"):
            msg = "update_account: server returned empty account"
            raise RuntimeError(msg)
        return map_account(res.account)

    async def delete(self, id_: str) -> None:
        req = DeleteAccountRequest(name=account_name(id_))
        await self._client.delete_account(req)

    async def resolve(self, *, external_id: str) -> Account:
        req = ResolveAccountRequest(external_id=external_id)
        res = await self._client.resolve_account(req)
        if not res.HasField("account"):
            msg = "resolve_account: server returned empty account"
            raise RuntimeError(msg)
        return map_account(res.account)

    async def claim(self, *, id_: str, contact_id: str, request_id: str = "") -> Account:
        req = ClaimAccountRequest(
            name=account_name(id_),
            contact_id=contact_id,
            request_id=request_id,
        )
        res = await self._client.claim_account(req)
        if not res.HasField("account"):
            msg = "claim_account: server returned empty account"
            raise RuntimeError(msg)
        return map_account(res.account)
