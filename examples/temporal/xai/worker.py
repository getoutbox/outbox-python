# Agent using Outbox Temporal destination + xAI

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from activity import process_message
from outbox_sdk import DestinationEventType, OutboxClient
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import MessageHandlerWorkflow

TASK_QUEUE = "outbox-messages"
WORKFLOW_TYPE = "MessageHandlerWorkflow"


async def main() -> None:
    client = await Client.connect(os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"))

    # Register (or update) the destination — upsert semantics make this safe
    # to call on every startup without creating duplicates.
    outbox = OutboxClient(api_key=os.environ["OUTBOX_API_KEY"])
    await outbox.destinations.create(
        destination_id="temporal-xai",
        display_name="Temporal xAI agent",
        target_type="temporal",
        target_config={
            "address": os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"),
            "namespace": os.environ.get("TEMPORAL_NAMESPACE", "default"),
            "task_queue": TASK_QUEUE,
            "workflow_type": WORKFLOW_TYPE,
            "api_key": os.environ.get("TEMPORAL_API_KEY", ""),
        },
        event_types=[DestinationEventType.MESSAGE],
    )

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[MessageHandlerWorkflow],
        activities=[process_message],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
