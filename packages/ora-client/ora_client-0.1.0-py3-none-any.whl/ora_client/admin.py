import asyncio
from typing import AsyncGenerator, Iterable, Literal

from grpclib.client import Channel
from pydantic import BaseModel, TypeAdapter

from ora_client.job_definition import JobDefinition
from ora_client.proto.ora.common.v1 import (
    JobDefinition as JobDefinitionProto,
)
from ora_client.proto.ora.common.v1 import (
    JobLabel,
    JobRetryPolicy,
    JobTimeoutBaseTime,
    JobTimeoutPolicy,
)
from ora_client.proto.ora.server.v1 import (
    AdminServiceStub,
    CancelJobsRequest,
    CreateJobsRequest,
    Job,
    JobExecutionStatus,
    JobLabelFilter,
    JobQueryFilter,
    JobQueryOrder,
    LabelFilterExistCondition,
    ListJobsRequest,
)


class JobHandle:
    """
    A handle to a job.
    """

    def __init__(
        self, job_id: str, client: AdminServiceStub, cached_job: Job | None = None
    ):
        self._job_id = job_id
        self._client = client
        self._cached_details = cached_job

    @property
    def id(self) -> str:
        """
        The ID of the job.
        """
        return self._job_id

    async def details(self) -> Job:
        """
        Get the details of the job.
        """
        if self._cached_details is not None and not self._cached_details.active:
            return self._cached_details

        res = await self._client.list_jobs(
            ListJobsRequest(
                filter=JobQueryFilter(
                    active=True,
                    job_ids=[self._job_id],
                )
            )
        )

        if len(res.jobs) != 1:
            raise RuntimeError("job not found")

        self._cached_details = res.jobs[0]

        return self._cached_details

    async def result[T](
        self,
        cls: type[T],
        poll_interval_seconds: float = 1.0,
    ) -> T | None:
        """
        Get the result of the job and deserialize it
        with the given class.
        """

        while True:
            job = await self.details()

            if job.active:
                await asyncio.sleep(poll_interval_seconds)
                continue

            break

        try:
            last_execution = job.executions[-1]
        except IndexError:
            return None

        if last_execution.output_payload_json is None:
            return None

        if issubclass(cls, BaseModel):
            return cls.model_validate_json(last_execution.output_payload_json)

        return TypeAdapter(cls).validate_json(last_execution.output_payload_json)

    async def cancel(self) -> None:
        """
        Cancel the job.
        """
        await self._client.cancel_jobs(
            CancelJobsRequest(
                filter=JobQueryFilter(
                    active=True,
                    job_ids=[self._job_id],
                )
            )
        )


class AdminClient:
    """
    A high-level client for the admin service.
    """

    def __init__(self, channel: Channel):
        self._channel = channel
        self._client = AdminServiceStub(channel)

    async def add_jobs(
        self, *jobs: JobDefinition | Iterable[JobDefinition]
    ) -> list[JobHandle]:
        """
        Add jobs to the job queue.
        """
        jobs_flat: list[JobDefinition] = []

        for job in jobs:
            if isinstance(job, Iterable):
                jobs_flat.extend(job)
            else:
                jobs_flat.append(job)

        res = await self._client.create_jobs(
            CreateJobsRequest(
                jobs=[
                    JobDefinitionProto(
                        job_type_id=job.job_type_id,
                        target_execution_time=job.target_execution_time,
                        input_payload_json=job.input_payload_json,
                        labels=[
                            JobLabel(
                                key=label[0],
                                value=label[1],
                            )
                            for label in job.labels.items()
                        ],
                        timeout_policy=JobTimeoutPolicy(
                            timeout=job.timeout_policy.timeout,
                            base_time=JobTimeoutBaseTime(job.timeout_policy.base_time),
                        ),
                        retry_policy=JobRetryPolicy(job.retry_policy.retries),
                        metadata_json=job.metadata_json,
                    )
                    for job in jobs_flat
                ]
            )
        )

        if len(res.job_ids) != len(jobs_flat):
            raise RuntimeError("failed to create all jobs")

        return [JobHandle(job_id=job_id, client=self._client) for job_id in res.job_ids]

    def job(self, job_id: str) -> JobHandle:
        """
        Get a handle to a job.

        Note that this does not check if the job exists.
        """
        return JobHandle(job_id=job_id, client=self._client)

    async def jobs(
        self,
        job_ids: list[str] | None,
        job_type_ids: list[str] | None,
        execution_ids: list[str] | None,
        schedule_ids: list[str] | None,
        status: list["JobExecutionStatus"] | None,
        labels: dict[str, str | Literal[True]] | None,
        active: bool | None,
        order: Literal[
            "created_asc", "created_desc", "target_asc", "target_desc"
        ] = "created_asc",
        buffer_size: int = 100,
    ) -> AsyncGenerator[JobHandle, None]:
        """
        Retrieve jobs based on the given filters.

        The returned job handles will have their details cached.
        """
        filter = JobQueryFilter()

        if job_ids is not None:
            filter.job_ids = job_ids

        if job_type_ids is not None:
            filter.job_type_ids = job_type_ids

        if execution_ids is not None:
            filter.execution_ids = execution_ids

        if schedule_ids is not None:
            filter.schedule_ids = schedule_ids

        if status is not None:
            filter.status = status

        if labels is not None:
            filter.labels = []

            for key, value in labels.items():
                if value is True:
                    filter.labels.append(
                        JobLabelFilter(key=key, exists=LabelFilterExistCondition.EXISTS)
                    )
                else:
                    filter.labels.append(JobLabelFilter(key=key, equals=value))

        if active is not None:
            filter.active = active

        match order:
            case "created_asc":
                order_option = JobQueryOrder.CREATED_AT_ASC
            case "created_desc":
                order_option = JobQueryOrder.CREATED_AT_DESC
            case "target_asc":
                order_option = JobQueryOrder.TARGET_EXECUTION_TIME_ASC
            case "target_desc":
                order_option = JobQueryOrder.TARGET_EXECUTION_TIME_DESC

        cursor = None

        while True:
            res = await self._client.list_jobs(
                ListJobsRequest(
                    filter=filter,
                    order=order_option,
                    cursor=cursor,
                    limit=buffer_size,
                )
            )

            for job in res.jobs:
                yield JobHandle(
                    job_id=job.id,
                    client=self._client,
                    cached_job=job,
                )

            if not res.has_more:
                break

            cursor = res.cursor

    async def cancel_jobs(
        self,
        job_ids: list[str] | None = None,
        job_type_ids: list[str] | None = None,
        execution_ids: list[str] | None = None,
        schedule_ids: list[str] | None = None,
        status: list["JobExecutionStatus"] | None = None,
        labels: dict[str, str | Literal[True]] | None = None,
        active: bool | None = None,
    ):
        """
        Cancel jobs based on the given filters.
        """
        filter = JobQueryFilter()

        if job_ids is not None:
            filter.job_ids = job_ids

        if job_type_ids is not None:
            filter.job_type_ids = job_type_ids

        if execution_ids is not None:
            filter.execution_ids = execution_ids

        if schedule_ids is not None:
            filter.schedule_ids = schedule_ids

        if status is not None:
            filter.status = status

        if labels is not None:
            filter.labels = []

            for key, value in labels.items():
                if value is True:
                    filter.labels.append(
                        JobLabelFilter(key=key, exists=LabelFilterExistCondition.EXISTS)
                    )
                else:
                    filter.labels.append(JobLabelFilter(key=key, equals=value))

        if active is not None:
            filter.active = active

        await self._client.cancel_jobs(
            CancelJobsRequest(
                filter=filter,
            )
        )

    def inner(self):
        return self._client
