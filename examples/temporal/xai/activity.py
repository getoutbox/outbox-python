# Activity: Outbox + xAI (runs outside the Temporal sandbox — network I/O is allowed)

import os

from openai import AsyncOpenAI
from outbox_sdk import MessageDirection, MessagePart, OutboxClient, parse
from temporalio import activity

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
xai_client = AsyncOpenAI(
    api_key=os.environ["XAI_API_KEY"],
    base_url="https://api.x.ai/v1",
)


@activity.defn
async def process_message(payload: dict) -> None:
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
