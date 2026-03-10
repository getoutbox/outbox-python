# outbox-sdk

Python SDK for [Outbox](https://outbox.chat) — a unified messaging API for AI agents.

Send and receive messages across channels (Slack, WhatsApp, and more) with a single API. Fully async with type-safe interfaces.

## Installation

```bash
pip install outbox-sdk
```

Requires Python 3.11 or later.

## Quick start

```python
from outbox_sdk import OutboxClient

async with OutboxClient(api_key="ob_live_your_api_key") as client:
    result = await client.messages.send(
        connector_id="conn123",
        recipient_id="acct456",
        parts=[{"content_type": "text/plain", "content": b"Hello!"}],
    )
    print("sent:", result.id)
```

## Services

The client exposes five namespaces:

| Namespace | Description |
|-----------|-------------|
| `client.connectors` | Create and manage connectors (one per channel account) |
| `client.accounts` | Look up or manage end-user accounts |
| `client.messages` | Send, update, delete, and list messages |
| `client.destinations` | Configure push targets for delivery events |
| `client.channels` | List available messaging channels |

## Webhook verification

Verify and parse incoming webhook payloads:

```python
from outbox_sdk import verify, parse

valid = verify(body=raw_body, secret=signing_secret, signature=sig_header)

if not valid:
    raise HTTPException(status_code=401)

event = parse(raw_body)

if event.type == "message":
    print("message from connector:", event.connector_id)
elif event.type == "delivery_update":
    print("delivery update:", event.delivery_update.status)
elif event.type == "read_receipt":
    print("read receipt:", event.read_receipt.message_ids)
elif event.type == "typing_indicator":
    print("typing:", event.typing_indicator.typing)
```

## Helpers

| Function | Description |
|----------|-------------|
| `parse(body)` | Parse a delivery event from binary or JSON dict |
| `verify(body, secret, signature)` | Verify an HMAC-SHA256 webhook signature |
| `parse_id(resource_name)` | Extract the plain ID from a resource name |

## Client options

```python
client = OutboxClient(
    api_key="ob_live_your_api_key",
    base_url="https://custom-api.example.com",
)
```

The client is an async context manager that cleanly closes all connections on exit.

## License

MIT
