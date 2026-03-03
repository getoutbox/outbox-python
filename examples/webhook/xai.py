# Agent using Outbox webhook destination + xAI

import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from openai import AsyncOpenAI
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse, verify

logger = logging.getLogger(__name__)

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # Register (or update) the destination — upsert semantics make this safe
    # to call on every startup without creating duplicates.
    await outbox.destinations.create(
        destination_id="webhook-xai",
        display_name="Webhook xAI agent",
        target_type="webhook",
        target_config={
            "url": "https://your-server.example.com/inbound",
            "signing_secret": os.environ["OUTBOX_SIGNING_SECRET"],
        },
        event_types=[DestinationEventType.MESSAGE],
    )
    yield


app = FastAPI(lifespan=lifespan)
xai_client = AsyncOpenAI(api_key=os.environ["XAI_API_KEY"], base_url="https://api.x.ai/v1")


@app.post("/inbound")
async def inbound(request: Request, background_tasks: BackgroundTasks) -> dict[str, bool]:
    raw_body = await request.body()
    sig = request.headers.get("x-outbox-signature", "")
    if not verify(
        body=raw_body,
        secret=os.environ["OUTBOX_SIGNING_SECRET"],
        signature=sig,
    ):
        raise HTTPException(status_code=401)
    payload = await request.json()
    background_tasks.add_task(process_event, payload)
    return {"ok": True}


async def process_event(payload: dict) -> None:
    try:
        event = parse(payload)
        if event.type != "message":
            return

        connector_id = event.connector_id
        msg = event.message
        if msg.account is None:
            return
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
    except Exception:
        logger.exception("Failed to process message")
