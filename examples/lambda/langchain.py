# Agent using Outbox Lambda destination + LangChain

import asyncio
import json
import os

from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
llm = ChatOpenAI(model="gpt-5.2")


# Run once to register (or update) the Lambda destination.
# Upsert semantics mean it is safe to call on every cold start.
async def register_destination() -> None:
    await outbox.destinations.create(
        destination_id="lambda-langchain",
        display_name="Lambda LangChain agent",
        target_type="lambda",
        target_config={
            "url": os.environ["LAMBDA_FUNCTION_URL"],
        },
        event_types=[DestinationEventType.MESSAGE],
    )


# Lambda entry point — Outbox POSTs the event to the function URL.
def handler(event: dict, _context: object) -> dict:
    payload = json.loads(event.get("body") or "{}")
    asyncio.run(process_event(payload))
    return {"statusCode": 200, "body": "ok"}


async def process_event(payload: dict) -> None:
    event = parse(payload)
    if event.type != "message":
        return

    connector_id = event.connector_id
    msg = event.message
    user_text = msg.parts[0].text_content
    if msg.account is None:
        return
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
        lc_messages = [
            HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
            for m in history
        ] + [HumanMessage(content=user_text)]
        response = await llm.ainvoke(lc_messages)
        reply_text = str(response.content)

    await outbox.messages.send(
        connector_id=connector_id,
        account=sender_id,
        parts=[MessagePart.text(reply_text)],
    )


if __name__ == "__main__":
    asyncio.run(register_destination())
