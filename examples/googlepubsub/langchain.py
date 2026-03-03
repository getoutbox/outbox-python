# Agent using Outbox Google Pub/Sub destination + LangChain

import asyncio
import json
import logging
import os

from google.cloud import pubsub_v1
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

logger = logging.getLogger(__name__)

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
llm = ChatOpenAI(model="gpt-5.2")

PROJECT_ID = os.environ["GOOGLE_PROJECT_ID"]
SUBSCRIPTION_ID = os.environ.get("PUBSUB_SUBSCRIPTION", "outbox-events-sub")


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
        lc_messages = [
            HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
            for m in history
        ]
        response = await llm.ainvoke(lc_messages)
        reply_text = response.content

    await outbox.messages.send(
        connector_id=connector_id,
        account=account_id,
        parts=[MessagePart.text(reply_text)],
    )


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    try:
        payload = json.loads(message.data.decode())
        asyncio.run(process_event(payload))
    except Exception:
        logger.exception("Failed to process message")
    finally:
        message.ack()


def main() -> None:
    asyncio.run(outbox.destinations.create(
        destination_id="pubsub-langchain",
        display_name="Pub/Sub LangChain agent",
        target_type="google_pub_sub",
        target_config={
            "project_id": PROJECT_ID,
            "topic_id": "outbox-events",
        },
        event_types=[DestinationEventType.MESSAGE],
    ))
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    with subscriber:
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
            streaming_pull_future.result()


if __name__ == "__main__":
    main()
