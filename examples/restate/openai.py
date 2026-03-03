# Agent using Outbox Restate destination + OpenAI

import asyncio
import os

import restate
from openai import AsyncOpenAI
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

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
        response = await openai_client.chat.completions.create(
            model="gpt-5.2",
            messages=history,
        )
        reply_text = response.choices[0].message.content or ""

    await outbox.messages.send(
        connector_id=connector_id,
        account=sender_id,
        parts=[MessagePart.text(reply_text)],
    )


app = restate.app(services=[svc])

# Run with: hypercorn openai:app --bind 0.0.0.0:9080

if __name__ == "__main__":
    asyncio.run(
        outbox.destinations.create(
            destination_id="restate-openai",
            display_name="Restate OpenAI agent",
            target_type="restate",
            target_config={
                "url": "https://restate.example.com/MessageService/handleEvent",
            },
            event_types=[DestinationEventType.MESSAGE],
        )
    )
