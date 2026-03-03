# Agent using Outbox Inngest destination + Gemini

import asyncio
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import inngest
import inngest.fast_api
from fastapi import FastAPI
from google import genai
from google.genai import types
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
gemini = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

inngest_client = inngest.Inngest(
    app_id="gemini-agent",
    signing_key=os.environ.get("INNGEST_SIGNING_KEY"),
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # Register (or update) the destination — upsert semantics make this safe
    # to call on every startup without creating duplicates.
    await outbox.destinations.create(
        destination_id="inngest-gemini",
        display_name="Inngest Gemini agent",
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
        gemini_history = [
            types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[types.Part.from_text(text=m["content"])],
            )
            for m in history
        ]
        chat = gemini.chats.create(model="gemini-3.1-pro-preview", history=gemini_history)
        response = await asyncio.to_thread(chat.send_message, user_text)
        reply_text = response.text

    await outbox.messages.send(
        connector_id=connector_id,
        account=sender_id,
        parts=[MessagePart.text(reply_text)],
    )


inngest.fast_api.serve(app, inngest_client, [handle_outbox_message])
