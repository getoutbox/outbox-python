# Agent using Outbox SNS destination + LangChain

import asyncio
import json
import os

from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
llm = ChatOpenAI(model="gpt-5.2")


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
        lc_messages = [
            HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
            for m in history
        ]
        response = await llm.ainvoke(lc_messages)
        reply_text = response.content

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
