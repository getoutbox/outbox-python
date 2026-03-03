# outbox-python

Python SDK monorepo for [Outbox](https://outbox.chat) — a unified messaging API for AI agents.

Send and receive messages across channels (Slack, WhatsApp, and more) with a single API.

## Packages

| Package | Description |
|---------|-------------|
| [`outbox-sdk`](packages/sdk/) | Async Outbox client SDK for Python 3.11+ |

## Getting started

See the SDK package for installation and usage: [`packages/sdk/`](packages/sdk/).

## Development

This monorepo uses [uv](https://docs.astral.sh/uv/) workspaces.

```bash
uv sync
uv run pytest
uv run pyright
uv run ruff check
```

## Examples

See the [`examples/`](examples/) directory for integration examples with:

EventBridge, Google Pub/Sub, Hatchet, Inngest, Kafka, Lambda, NATS, Restate, SNS, SQS, Temporal, Webhooks

## License

MIT
