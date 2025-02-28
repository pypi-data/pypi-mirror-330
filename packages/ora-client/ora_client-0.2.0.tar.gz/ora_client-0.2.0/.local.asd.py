import asyncio
from datetime import UTC, datetime, timedelta

from grpclib.client import Channel

from ora_client.admin import AdminClient
from ora_client.executor import ExecutionContext, Executor, handler
from ora_client.job_type import JobType


class PrintValue(JobType[str]):
    """
    Print a value and return it.
    """

    value: str


@handler
async def handle_print_value(context: ExecutionContext, job: PrintValue) -> str:
    print(context.target_execution_time)
    print("latency:", datetime.now(UTC) - context.target_execution_time)
    print(job.value)
    return job.value


executor = Executor(
    name="my-executor",
    max_concurrent=1,
)

executor.handle(PrintValue, handle_print_value)


def spawn_executor():
    async def _executor():
        while True:
            try:
                async with Channel(host="localhost", port=50051) as channel:
                    await executor.run(channel)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                print(e)
                await asyncio.sleep(1)

    asyncio.create_task(_executor())


async def main():
    async with Channel(host="localhost", port=50051) as channel:
        client = AdminClient(channel)

    # await client.remove_inactive_schedules()
    # await client.remove_inactive_jobs()

    async for job in client.jobs(
        labels={"project_id": "foo"},
    ):
        print(job.id)

    if await client.schedule_exists(labels={"project_id": "foo"}, active=True):
        await client.cancel_schedules(labels={"project_id": "foo"})
    else:
        print("schedule does not exist")

        await client.add_schedules(
            PrintValue(
                value="hello",
            )
            .job()
            .repeat(timedelta(seconds=1))
            .immediate(True)
            .with_labels(project_id="foo")
        )

    spawn_executor()

    await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
