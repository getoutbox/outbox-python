# Agent using Outbox Kafka destination + LangChain

import asyncio
import json
import logging
import os

from aiokafka import AIOKafkaConsumer
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

logger = logging.getLogger(__name__)

# --- Initialize clients ---
outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
llm = ChatOpenAI(model="gpt-5.2")

# --- Kafka configuration ---
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
TOPIC = os.environ.get("KAFKA_TOPIC", "outbox-events")


async def main() -> None:
    # --- Register the destination ---
    await outbox.destinations.create(
        destination_id="kafka-langchain",
        display_name="Kafka LangChain agent",
        target_type="kafka",
        target_config={
            "brokers": KAFKA_BROKER,
            "topic": TOPIC,
        },
        event_types=[DestinationEventType.MESSAGE],
    )

    # --- Create and start the consumer ---
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id="outbox-agent",
        value_deserializer=json.loads,
    )
    await consumer.start()
    try:
        # --- Consume messages ---
        async for msg in consumer:
            try:
                # --- Parse the event ---
                event = parse(msg.value)
                if event.type != "message":
                    continue

                connector_id = event.connector_id
                outbox_msg = event.message
                sender_id = outbox_msg.account.id

                # --- Acknowledge the message ---
                await outbox.messages.mark_read(
                    connector_id=connector_id,
                    account_id=sender_id,
                    messages=[outbox_msg.id],
                )

                # --- Fetch conversation history ---
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

                # --- Generate a reply ---
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

                # --- Send the reply ---
                await outbox.messages.send(
                    connector_id=connector_id,
                    account=sender_id,
                    parts=[MessagePart.text(reply_text)],
                )
            except Exception:
                logger.exception("Failed to process message")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
