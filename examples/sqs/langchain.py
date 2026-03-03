# Agent using Outbox SQS destination + LangChain

import asyncio
import json
import os

import boto3
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

sqs = boto3.client("sqs", region_name=os.environ.get("AWS_REGION", "us-east-1"))
QUEUE_URL = os.environ["SQS_QUEUE_URL"]
outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
llm = ChatOpenAI(model="gpt-5.2")


async def poll() -> None:
    # Register (or update) the destination — upsert semantics make this safe
    # to call on every startup without creating duplicates.
    await outbox.destinations.create(
        destination_id="sqs-langchain",
        display_name="SQS LangChain agent",
        target_type="sqs",
        target_config={
            "queue_url": QUEUE_URL,
            "region": os.environ.get("AWS_REGION", "us-east-1"),
            "access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
        },
        event_types=[DestinationEventType.MESSAGE],
    )
    while True:
        response = await asyncio.to_thread(
            sqs.receive_message,
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20,
        )
        messages = response.get("Messages", [])
        await asyncio.gather(*[handle_sqs_message(m) for m in messages])


async def handle_sqs_message(sqs_msg: dict) -> None:
    payload = json.loads(sqs_msg["Body"])
    await process_event(payload)
    await asyncio.to_thread(
        sqs.delete_message,
        QueueUrl=QUEUE_URL,
        ReceiptHandle=sqs_msg["ReceiptHandle"],
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


if __name__ == "__main__":
    asyncio.run(poll())
