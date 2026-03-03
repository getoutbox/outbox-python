# Temporal workflow for Outbox message handling

from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activity import process_message


@workflow.defn
class MessageHandlerWorkflow:
    @workflow.run
    async def run(self, payload: dict) -> None:
        await workflow.execute_activity(
            process_message,
            payload,
            start_to_close_timeout=timedelta(seconds=30),
        )
