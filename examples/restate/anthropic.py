# Agent using Outbox Restate destination + Anthropic

import asyncio
import os

import anthropic
import restate
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
anthropic_client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

svc = restate.Service("MessageService")


@svc.handler()
async def handle_event(_ctx: restate.Context, payload: dict) -> None:
    event = parse(payload)
    if event.type != "message":
        return

    connector_id = event.connector_id
    msg = event.message
    sender_id = msg.account.id

    await outbox.messages.mark_read(
        connector_id=connector_id,
        account_id=sender_id,
        messages=[msg.id],
    )

    result = await outbox.messages.history(
        connector_id=connector_id,
        account_id=sender_id,
        page_size=20,
    )
    history = [
        {
            "role": "user" if m.direction == MessageDirection.INBOUND else "assistant",
            "content": m.parts[0].text_content,
        }
        for m in result.items
    ]

    async with outbox.messages.typing_indicator(
        connector_id=connector_id,
        account_id=sender_id,
    ):
        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=history,
        )
        reply_text = response.content[0].text

    await outbox.messages.send(
        connector_id=connector_id,
        account=sender_id,
        parts=[MessagePart.text(reply_text)],
    )


app = restate.app(services=[svc])

# Run with: hypercorn anthropic:app --bind 0.0.0.0:9080

if __name__ == "__main__":
    asyncio.run(
        outbox.destinations.create(
            destination_id="restate-anthropic",
            display_name="Restate Anthropic agent",
            target_type="restate",
            target_config={
                "url": "https://restate.example.com/MessageService/handleEvent",
            },
            event_types=[DestinationEventType.MESSAGE],
        )
    )
