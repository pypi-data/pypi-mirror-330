#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/11/1
# @Author  : zhoubohan
# @File    : tracker.py
"""

import atexit
import os
import queue
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Union, List

from jobv1.client.job_api_event import CreateEventRequest, EventKind
from jobv1.client.job_api_job import parse_job_name
from jobv1.client.job_api_metric import (
    CreateMetricRequest,
    MetricLocalName,
    MetricKind,
    CounterKind,
    DataType,
)
from jobv1.client.job_api_task import CreateTaskRequest, parse_task_name
from jobv1.client.job_client import JobClient
from windmillclient.client.windmill_client import WindmillClient


class Tracker:
    """Tracker is an agent to track metrics & events asynchronously."""

    def __init__(
        self,
        client: Optional[Union[WindmillClient, JobClient]] = None,
        workspace_id: Optional[str] = None,
        job_name: Optional[str] = None,
        task_name: Optional[str] = None,
    ):
        """Initialize a new Tracker instance."""
        self._workspace_id = workspace_id or os.getenv("WORKSPACE_ID")
        self._job_name = job_name or os.getenv("JOB_NAME")
        self._task_name = task_name or os.getenv("TASK_NAME")

        self._client = client if client else self._initialize_client()
        self._validate_client()

        if self._job_name:
            self.set_job_name(self._job_name)

        if self._task_name:
            self.set_task_name(self._task_name)

        self._queue = queue.Queue(maxsize=1000)
        self._shutdown_flag = False
        self._executor = None
        self._initialize_worker()

        atexit.register(self._cleanup)

    def _initialize_worker(self):
        """_initialize_worker"""
        if self._executor is None:
            self._executor = ThreadPoolExecutor(
                max_workers=1, thread_name_prefix="TrackerThread"
            )
            self._executor.submit(self._process_queue)

    def _process_queue(self):
        """Process requests in the queue asynchronously with proper thread management."""
        while not self._shutdown_flag:
            try:
                func, args = self._queue.get(timeout=0.5)
                if func is None:
                    break
                func(args)
            except queue.Empty:
                continue
            finally:
                self._queue.task_done()

    def _cleanup(self):
        """cleanup resources and ensure all queued items are processed"""
        if not self._shutdown_flag:
            # Wait for existing items in the queue to be processed
            if hasattr(self, '_queue') and self._queue:
                try:
                    self._queue.join()  # Wait until all queue items are processed
                except:
                    pass  # Continue with cleanup if join fails

            # Set shutdown flag to stop accepting new items
            self._shutdown_flag = True

            # Add sentinel value to unblock the worker thread
            self._queue.put((None, None))

            # Shutdown the executor
            if self._executor:
                self._executor.shutdown(wait=True)  # Wait for the executor to finish

    @staticmethod
    def _initialize_client() -> JobClient:
        """Initialize the JobClient using environment variables."""
        endpoint = os.getenv("WINDMILL_ENDPOINT")
        org_id = os.getenv("ORG_ID")
        user_id = os.getenv("USER_ID")

        if not all([endpoint, org_id, user_id]):
            raise ValueError(
                "Environment variables WINDMILL_ENDPOINT, ORG_ID, and USER_ID must be set "
                "when client is not provided."
            )

        return JobClient(
            endpoint=endpoint, context={"OrgID": org_id, "UserID": user_id}
        )

    def _validate_client(self):
        """Validate the provided client instance."""
        if not isinstance(self._client, (WindmillClient, JobClient)):
            raise TypeError(
                f"Client must be either WindmillClient or JobClient, got {type(self._client)}"
            )

    def set_job_name(self, job_name: str):
        """Set job name and update workspace ID if parsed successfully."""
        parsed = parse_job_name(job_name)
        self._job_name = parsed.local_name if parsed else job_name
        self._workspace_id = parsed.workspace_id if parsed else self._workspace_id

    def set_task_name(self, task_name: str):
        """Set task name and update job and workspace IDs if parsed successfully."""
        parsed = parse_task_name(task_name)
        self._task_name = parsed.local_name if parsed else task_name
        self._job_name = parsed.job_name if parsed else self._job_name
        self._workspace_id = parsed.workspace_id if parsed else self._workspace_id

    def _set_request_defaults(self, request, **kwargs):
        """Set job_name and task_name for request with explicit argument distinction."""
        request.workspace_id = self._workspace_id

        job_name = kwargs.get("job_name", self._job_name)
        if job_name not in (None, ""):
            parsed = parse_job_name(job_name)
            job_name = parsed.local_name if parsed else job_name
            request.workspace_id = (
                parsed.workspace_id if parsed else request.workspace_id
            )
            request.job_name = job_name

        if request.field_exists("task_name"):
            task_name = kwargs.get("task_name", self._task_name)
            if task_name not in (None, ""):
                parsed = parse_task_name(task_name)
                task_name = parsed.local_name if parsed else task_name
                job_name = parsed.job_name if parsed else job_name
                request.workspace_id = (
                    parsed.workspace_id if parsed else request.workspace_id
                )

            request.job_name = job_name
            request.task_name = task_name

    def create_task(
        self,
        kind: str,
        local_name: Optional[str] = None,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        order: Optional[int] = 0,
        **kwargs,
    ):
        """Create a task with the given parameters."""
        request = CreateTaskRequest(
            kind=kind,
            local_name=local_name,
            display_name=display_name,
            description=description,
            order=order,
        )
        self._set_request_defaults(request, **kwargs)
        self._queue.put((self._client.create_task, request))

    def log_metric(
        self,
        value: List[str],
        local_name: MetricLocalName = MetricLocalName.Status,
        kind: MetricKind = MetricKind.Gauge,
        data_type: DataType = DataType.String,
        counter_kind: CounterKind = CounterKind.Cumulative,
        **kwargs,  # 让 job_name 和 task_name 通过 kwargs 传递
    ):
        """Log a metric for the given job/task. Does not modify instance attributes."""
        request = CreateMetricRequest(
            value=value,
            local_name=local_name,
            kind=kind,
            data_type=data_type,
            counter_kind=counter_kind,
        )

        self._set_request_defaults(request, **kwargs)  # 直接传 kwargs
        self._queue.put((self._client.create_metric, request))

    def log_event(
        self,
        reason: str,
        message: str,
        kind: Optional[EventKind] = EventKind.Normal,
        **kwargs,  # 让 job_name 和 task_name 通过 kwargs 传递
    ):
        """Log an event for the given job/task. Does not modify instance attributes."""
        request = CreateEventRequest(
            reason=reason,
            message=message,
            kind=kind,
        )
        self._set_request_defaults(request, **kwargs)  # 直接传 kwargs
        self._queue.put((self._client.create_event, request))
