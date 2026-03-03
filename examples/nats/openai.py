import asyncio
import json
import logging
import os

import nats
from nats.aio.msg import Msg
from openai import AsyncOpenAI
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

logger = logging.getLogger(__name__)

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

NATS_URL = os.environ.get("NATS_URL", "nats://localhost:4222")
SUBJECT = os.environ.get("NATS_SUBJECT", "outbox.events")


async def process_event(payload: dict) -> None:
    event = parse(payload)
    if event.type != "message":
        return

    connector_id = event.connector_id
    msg = event.message
    account_id = msg.account.id

    await outbox.messages.mark_read(
        connector_id=connector_id,
        account_id=account_id,
        messages=[msg.id],
    )

    result = await outbox.messages.history(
        connector_id=connector_id,
        account_id=account_id,
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
        account_id=account_id,
    ):
        response = await openai_client.chat.completions.create(
            model="gpt-5.2",
            messages=history,
        )
        reply_text = response.choices[0].message.content or ""

    await outbox.messages.send(
        connector_id=connector_id,
        account=account_id,
        parts=[MessagePart.text(reply_text)],
    )


async def message_handler(msg: Msg) -> None:
    try:
        payload = json.loads(msg.data.decode())
        await process_event(payload)
    except Exception:
        logger.exception("Failed to process message")


async def main() -> None:
    await outbox.destinations.create(
        destination_id="nats-openai",
        display_name="NATS OpenAI agent",
        target_type="nats",
        target_config={
            "url": NATS_URL,
            "subject": SUBJECT,
        },
        event_types=[DestinationEventType.MESSAGE],
    )

    nc = await nats.connect(NATS_URL)
    await nc.subscribe(SUBJECT, cb=message_handler)
    try:
        await asyncio.Event().wait()
    finally:
        await nc.drain()


if __name__ == "__main__":
    asyncio.run(main())
