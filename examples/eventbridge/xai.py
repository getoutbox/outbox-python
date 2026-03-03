# Agent using Outbox EventBridge destination + xAI

import asyncio
import os

from openai import AsyncOpenAI
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
xai_client = AsyncOpenAI(api_key=os.environ["XAI_API_KEY"], base_url="https://api.x.ai/v1")


# Run once to register (or update) the EventBridge destination.
# Upsert semantics mean it is safe to call on every cold start.
async def register_destination() -> None:
    await outbox.destinations.create(
        destination_id="eventbridge-xai",
        display_name="EventBridge xAI agent",
        target_type="event_bridge",
        target_config={
            "event_bus": os.environ.get("EVENTBRIDGE_BUS", "default"),
            "region": os.environ.get("AWS_REGION", "us-east-1"),
            "access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
        },
        event_types=[DestinationEventType.MESSAGE],
    )


# Lambda entry point — EventBridge puts the Outbox payload in event["detail"].
def lambda_handler(event: dict, _context: object) -> None:
    payload = event.get("detail", {})
    asyncio.run(process_event(payload))


async def process_event(payload: dict) -> None:
    event = parse(payload)
    if event.type != "message":
        return

    connector_id = event.connector_id
    msg = event.message
    user_text = msg.parts[0].text_content
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
        response = await xai_client.chat.completions.create(
            model="grok-4",
            messages=[*history, {"role": "user", "content": user_text}],
        )
        reply_text = response.choices[0].message.content or ""

    await outbox.messages.send(
        connector_id=connector_id,
        account=sender_id,
        parts=[MessagePart.text(reply_text)],
    )


if __name__ == "__main__":
    asyncio.run(register_destination())
