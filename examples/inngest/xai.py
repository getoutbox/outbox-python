# Agent using Outbox Inngest destination + xAI

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import inngest
import inngest.fast_api
from fastapi import FastAPI
from openai import AsyncOpenAI
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
xai_client = AsyncOpenAI(
    api_key=os.environ["XAI_API_KEY"],
    base_url="https://api.x.ai/v1",
)

inngest_client = inngest.Inngest(
    app_id="xai-agent",
    signing_key=os.environ.get("INNGEST_SIGNING_KEY"),
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # Register (or update) the destination — upsert semantics make this safe
    # to call on every startup without creating duplicates.
    await outbox.destinations.create(
        destination_id="inngest-xai",
        display_name="Inngest xAI agent",
        target_type="inngest",
        target_config={
            "event_key": os.environ["INNGEST_EVENT_KEY"],
            "event_name": "outbox/message.received",
        },
        event_types=[DestinationEventType.MESSAGE],
    )
    yield


app = FastAPI(lifespan=lifespan)


@inngest_client.create_function(
    fn_id="handle-outbox-message",
    trigger=inngest.TriggerEvent(event="outbox/message.received"),
)
async def handle_outbox_message(ctx: inngest.Context) -> None:
    event = parse(ctx.event.data)
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
            messages=[*history, {"role": "user", "content": user_text}],  # type: ignore[arg-type]
        )
        reply_text = response.choices[0].message.content or ""

    await outbox.messages.send(
        connector_id=connector_id,
        account=sender_id,
        parts=[MessagePart.text(reply_text)],
    )


inngest.fast_api.serve(app, inngest_client, [handle_outbox_message])
