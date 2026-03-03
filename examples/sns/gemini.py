# Agent using Outbox SNS destination + Gemini

import asyncio
import json
import os

from google import genai
from google.genai import types
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
gemini = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


# Run once to register the destination before deploying the Lambda function.
# Upsert semantics mean it is safe to call on every deployment.
async def register() -> None:
    await outbox.destinations.create(
        destination_id="sns-agent",
        display_name="SNS agent",
        target_type="sns",
        target_config={
            "topic_arn": os.environ["SNS_TOPIC_ARN"],
            "region": os.environ.get("AWS_REGION", "us-east-1"),
            "access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
        },
        event_types=[DestinationEventType.MESSAGE],
    )


async def process_event(payload: dict) -> None:
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
        gemini_history = [
            types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[types.Part.from_text(text=m["content"])],
            )
            for m in history
        ]
        chat = gemini.chats.create(model="gemini-3.1-pro-preview", history=gemini_history)
        response = await asyncio.to_thread(chat.send_message, msg.parts[0].text_content)
        reply_text = response.text

    await outbox.messages.send(
        connector_id=connector_id,
        account=sender_id,
        parts=[MessagePart.text(reply_text)],
    )


def lambda_handler(event: dict, _context: object) -> None:
    async def process_all() -> None:
        for record in event.get("Records", []):
            payload = json.loads(record["Sns"]["Message"])
            await process_event(payload)

    asyncio.run(process_all())


if __name__ == "__main__":
    asyncio.run(register())
