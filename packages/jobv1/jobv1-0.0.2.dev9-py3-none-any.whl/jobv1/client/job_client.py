#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/10/31
# @Author  : zhoubohan
# @File    : job_client.py
"""
from typing import Optional

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.http import http_methods, http_content_types
from bceinternalsdk.client.bce_internal_client import BceInternalClient

from .job_api_event import (
    CreateEventRequest,
    CreateEventResponse,
    ListEventRequest,
    ListEventResponse,
)
from .job_api_job import (
    CreateJobRequest,
    CreateJobResponse,
    ListJobRequest,
    ListJobResponse,
    GetJobRequest,
    GetJobResponse,
    CountJobRequest,
    CountJobResponse,
    UpdateJobRequest,
    DeleteJobRequest,
    StopJobRequest,
    BatchStopJobRequest,
    BatchDeleteJobRequest,
    RecreateJobRequest,
)
from .job_api_metric import (
    ListMetricRequest,
    ListMetricResponse,
    GetMetricRequest,
    GetMetricResponse,
    UpdateMetricRequest,
    DeleteMetricRequest,
    CreateMetricRequest,
    CreateMetricResponse,
)
from .job_api_task import (
    CreateTaskRequest,
    CreateTaskResponse,
    ListTaskRequest,
    ListTaskResponse,
    GetTaskRequest,
    GetTaskResponse,
    UpdateTaskRequest,
    DeleteTaskRequest,
    StopTaskRequest,
)


class JobClient(BceInternalClient):
    """
    JobClient is the client for JobService API.
    """

    def __init__(
        self,
        config: Optional[BceClientConfiguration] = None,
        ak: Optional[str] = "",
        sk: Optional[str] = "",
        endpoint: Optional[str] = "",
        context: Optional[dict] = None,
    ):
        """
        Init
        :param config:
        :param ak:
        :param sk:
        :param endpoint:
        :param context:
        """
        self.__module__ = "windmilljob.jobv1.client"
        super(JobClient, self).__init__(
            config=config, ak=ak, sk=sk, endpoint=endpoint, context=context
        )

    @staticmethod
    def _build_base_task_uri(
        workspace_id: str, job_name: str, task_name: Optional[str] = None
    ) -> str:
        """
        Build the base uri for Task.
        :param workspace_id:
        :param job_name:
        :param task_name:
        :return:
        """
        base_uri = f"/v1/workspaces/{workspace_id}/jobs/{job_name}/tasks"

        if task_name is not None and len(task_name) > 0:
            base_uri = f"{base_uri}/{task_name}"

        return base_uri

    @staticmethod
    def _build_base_event_uri(
        workspace_id: str,
        job_name: str,
        task_name: Optional[str] = None,
        event_name: Optional[str] = None,
    ) -> str:
        """build the base uri for Event.
        /v1/workspaces/{workspace_id}/jobs/{job_name}/tasks/{task_name}/events/{event_name}
        /v1/workspaces/{workspace_id}/jobs/{job_name}/events/{event_name}
        /v1/workspaces/{workspace_id}/jobs/{job_name}/tasks/{task_name}/events
        /v1/workspaces/{workspace_id}/jobs/{job_name}/events

        Args:
            workspace_id (str): _description_
            job_name (str): _description_
            task_name (Optional[str], optional): _description_. Defaults to None.
            event_name (Optional[str], optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        base_uri = f"/v1/workspaces/{workspace_id}/jobs/{job_name}"

        if task_name is not None and len(task_name) > 0:
            base_uri = f"{base_uri}/tasks/{task_name}"

        base_uri = f"{base_uri}/events"

        if event_name is not None and len(event_name) > 0:
            base_uri = f"{base_uri}/{event_name}"

        return base_uri

    @staticmethod
    def _build_base_metric_uri(
        workspace_id: str,
        job_name: str,
        task_name: Optional[str] = None,
        metric_name: Optional[str] = None,
    ) -> str:
        """build the base uri for Metric.
        /v1/workspaces/{workspace_id}/jobs/{job_name}/tasks/{task_name}/metrics/{metric_name}
        /v1/workspaces/{workspace_id}/jobs/{job_name}/metrics/{metric_name}
        /v1/workspaces/{workspace_id}/jobs/{job_name}/tasks/{task_name}/metrics
        /v1/workspaces/{workspace_id}/jobs/{job_name}/metrics

        Args:
            workspace_id (str): _description_
            job_name (str): _description_
            task_name (Optional[str], optional): _description_. Defaults to None.
            metric_name (Optional[str], optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        base_uri = f"/v1/workspaces/{workspace_id}/jobs/{job_name}"

        if task_name is not None and len(task_name) > 0:
            base_uri = f"{base_uri}/tasks/{task_name}"

        base_uri = f"{base_uri}/metrics"

        if metric_name is not None and len(metric_name) > 0:
            base_uri = f"{base_uri}/{metric_name}"

        return base_uri

    def create_event(self, request: CreateEventRequest) -> CreateEventResponse:
        """
        Create a new Event.
        :return: None
        """
        response = self._send_request(
            http_method=http_methods.POST,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                self._build_base_event_uri(
                    request.workspace_id,
                    request.job_name,
                    request.task_name,
                ),
                encoding="utf-8",
            ),
            body=request.json().encode("utf-8"),
        )

        return CreateEventResponse.from_response(response)

    def list_event(self, request: ListEventRequest) -> ListEventResponse:
        """
        List events.
        """
        response = self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                self._build_base_event_uri(
                    request.workspace_id,
                    request.job_name,
                    request.task_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            params=request.json().encode("utf-8"),
        )

        return ListEventResponse.from_response(response)

    def create_metric(self, request: CreateMetricRequest) -> CreateMetricResponse:
        """
        Create a new Metric.
        :return: None
        """
        response = self._send_request(
            http_method=http_methods.POST,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                self._build_base_metric_uri(
                    request.workspace_id,
                    request.job_name,
                    request.task_name,
                ),
                encoding="utf-8",
            ),
            body=request.json().encode("utf-8"),
        )

        return CreateMetricResponse.from_response(response)

    def list_metric(self, request: ListMetricRequest) -> ListMetricResponse:
        """
        List metrics.
        """
        response = self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                self._build_base_metric_uri(
                    request.workspace_id,
                    request.job_name,
                    request.task_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            params=request.json().encode("utf-8"),
        )

        return ListMetricResponse.from_response(response)

    def get_metric(self, request: GetMetricRequest) -> GetMetricResponse:
        """
        Get a metric.
        """
        response = self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                self._build_base_metric_uri(
                    request.workspace_id,
                    request.job_name,
                    request.task_name,
                    request.local_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
        )

        return GetMetricResponse.from_response(response)

    def update_metric(self, request: UpdateMetricRequest):
        """
        Update a metric.
        """
        return self._send_request(
            http_method=http_methods.PUT,
            path=bytes(
                self._build_base_metric_uri(
                    request.workspace_id,
                    request.job_name,
                    request.task_name,
                    request.local_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=request.json().encode("utf-8"),
        )

    def delete_metric(self, request: DeleteMetricRequest):
        """
        Delete a metric.
        """
        return self._send_request(
            http_method=http_methods.DELETE,
            path=bytes(
                self._build_base_metric_uri(
                    request.workspace_id,
                    request.job_name,
                    request.task_name,
                    request.local_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
        )

    def create_task(self, request: CreateTaskRequest) -> CreateTaskResponse:
        """
        Create a new Task.
        """
        response = self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                self._build_base_task_uri(
                    request.workspace_id,
                    request.job_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=request.json().encode("utf-8"),
        )

        return CreateTaskResponse.from_response(response)

    def list_task(self, request: ListTaskRequest) -> ListTaskResponse:
        """
        List tasks.
        """
        response = self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                self._build_base_task_uri(
                    request.workspace_id,
                    request.job_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            params=request.json().encode("utf-8"),
        )

        return ListTaskResponse.from_response(response)

    def get_task(self, request: GetTaskRequest) -> GetTaskResponse:
        """
        Get a task.
        """
        response = self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                self._build_base_task_uri(
                    request.workspace_id,
                    request.job_name,
                    request.local_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
        )

        return GetTaskResponse.from_response(response)

    def update_task(self, request: UpdateTaskRequest):
        """
        Update a task.
        """
        return self._send_request(
            http_method=http_methods.PUT,
            path=bytes(
                self._build_base_task_uri(
                    request.workspace_id,
                    request.job_name,
                    request.local_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=request.json().encode("utf-8"),
        )

    def delete_task(self, request: DeleteTaskRequest):
        """
        Delete a task.
        """
        return self._send_request(
            http_method=http_methods.DELETE,
            path=bytes(
                self._build_base_task_uri(
                    request.workspace_id,
                    request.job_name,
                    request.local_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
        )

    def stop_task(self, request: StopTaskRequest):
        """
        Stop a task.
        """
        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                self._build_base_task_uri(
                    request.workspace_id,
                    request.job_name,
                    request.local_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
        )

    def create_job(self, request: CreateJobRequest) -> CreateJobResponse:
        """
        Create a new Job.
        """
        response = self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                f"/v1/workspaces/{request.workspace_id}/jobs",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=request.json().encode("utf-8"),
        )

        return CreateJobResponse.from_response(response)

    def list_job(self, request: ListJobRequest) -> ListJobResponse:
        """
        List jobs.
        """
        if request.workspace_id == "":
            uri = "/v1/jobs"
        else:
            uri = f"/v1/workspaces/{request.workspace_id}/jobs"

        response = self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                uri,
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            params=request.model_dump(),
        )

        return ListJobResponse.from_response(response)

    def get_job(self, request: GetJobRequest) -> GetJobResponse:
        """
        Get a job.
        """
        response = self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                f"/v1/workspaces/{request.workspace_id}/jobs/{request.local_name}",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
        )

        return GetJobResponse.from_response(response)

    def count_job(self, request: CountJobRequest) -> CountJobResponse:
        """
        Count jobs.
        """
        response = self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                f"/v1/workspaces/{request.filters.workspace_id}/jobs/count",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            params=request.json().encode("utf-8"),
        )

        return CountJobResponse.from_response(response)

    def update_job(self, request: UpdateJobRequest):
        """
        Update a job.
        """
        return self._send_request(
            http_method=http_methods.PUT,
            path=bytes(
                f"/v1/workspaces/{request.workspace_id}/jobs/{request.local_name}",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=request.json().encode("utf-8"),
        )

    def delete_job(self, request: DeleteJobRequest):
        """
        Delete a job.
        """
        return self._send_request(
            http_method=http_methods.DELETE,
            path=bytes(
                f"/v1/workspaces/{request.workspace_id}/jobs/{request.local_name}",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
        )

    def stop_job(self, request: StopJobRequest):
        """
        Stop a job.
        """
        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                f"/v1/workspaces/{request.workspace_id}/jobs/{request.local_name}/stop",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
        )

    def batch_stop_job(self, request: BatchStopJobRequest):
        """
        Batch stop jobs.
        """
        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                f"/v1/workspaces/{request.workspace_id}/jobs/stop",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=request.json().encode("utf-8"),
        )

    def batch_delete_job(self, request: BatchDeleteJobRequest):
        """
        Batch delete jobs.
        """
        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                f"/v1/workspaces/{request.workspace_id}/jobs/deletion",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=request.json().encode("utf-8"),
        )

    def recreate_job(self, request: RecreateJobRequest):
        """
        Recreate a job.
        """
        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                f"/v1/workspaces/{request.workspace_id}/jobs/{request.local_name}/recreate",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
        )
