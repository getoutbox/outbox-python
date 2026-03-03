# Agent using Outbox Hatchet destination + LangChain

import asyncio
import os

from hatchet_sdk import Context, Hatchet
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from outbox_sdk import DestinationEventType, MessageDirection, MessagePart, OutboxClient, parse

outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
llm = ChatOpenAI(model="gpt-5.2")

hatchet = Hatchet()


async def process_event(payload: dict) -> None:
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
        lc_messages = [
            HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
            for m in history
        ] + [HumanMessage(content=user_text)]
        response = await llm.ainvoke(lc_messages)
        reply_text = response.content

    await outbox.messages.send(
        connector_id=connector_id,
        account=sender_id,
        parts=[MessagePart.text(reply_text)],
    )


@hatchet.task(name="handle-message")
async def handle_message(payload: dict, _ctx: Context) -> None:
    await process_event(payload)


def main() -> None:
    # Register (or update) the destination — upsert semantics make this safe
    # to call on every startup without creating duplicates.
    asyncio.run(outbox.destinations.create(
        destination_id="hatchet-langchain",
        display_name="Hatchet LangChain agent",
        target_type="hatchet",
        target_config={
            "address": "grpc.hatchet.run:443",
            "workflow_name": "handle-message",
            "api_token": os.environ["HATCHET_API_TOKEN"],
        },
        event_types=[DestinationEventType.MESSAGE],
    ))
    worker = hatchet.worker("outbox-worker", workflows=[handle_message])
    worker.start()


if __name__ == "__main__":
    main()
