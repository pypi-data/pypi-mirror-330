#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/12/17
# @Author  : zhoubohan
# @File    : job_api_job.py
"""
import re
from datetime import datetime
from enum import Enum
from typing import Any, List, Dict, Optional, TypeAlias

from bceinternalsdk.client.base_model import BaseModel
from bceinternalsdk.client.paging import PagingRequest

from .job_api_base import JobStatus
from .job_api_event import Event
from .job_api_metric import Metric
from .job_api_task import Task, CreateTaskRequest

job_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/jobs/(?P<local_name>.+?)$"
)

job_name_extra_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/" "extrajobs/(?P<extra_id>.+?)$"
)


class SpecKind(Enum):
    """
    SpecKind is the kind of the job pipeline spec.
    """

    Local = "Local"
    PaddleFlow = "PaddleFlow"
    Argo = "Argo"
    Ray = "Ray"
    Kube = "Kube"


class JobName(BaseModel):
    """
    JobName is the unique identifier for a Job.
    """

    workspace_id: str
    local_name: Optional[str] = None
    extra_id: Optional[str] = None

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True

    def get_name(self):
        """
        Get the name of the Job.
        :return: str
        """
        if self.extra_id is not None and len(self.extra_id) > 0:
            return f"workspaces/{self.workspace_id}/extrajobs/{self.extra_id}"
        return f"workspaces/{self.workspace_id}/jobs/{self.local_name}"


def parse_job_name(name: str) -> Optional[JobName]:
    """
    Parse the JobName from the name string.
    :param name: str
    :return: Optional[JobName]
    """
    match = job_name_regex.match(name)
    if match:
        return JobName(**match.groupdict())

    extra_match = job_name_extra_regex.match(name)
    if extra_match:
        return JobName(**extra_match.groupdict())

    return None


class Job(BaseModel):
    """
    Job is the model of the job.
    """

    name: str
    local_name: str
    display_name: str
    description: str

    kind: str
    tags: Optional[Dict[str, Any]] = None
    callback_endpoint: Optional[str] = None
    timeout_in_second: Optional[int] = None
    source_job_name: str
    spec_kind: SpecKind
    spec_raw: str
    parameters: Optional[Dict[str, Any]] = None
    file_system_name: str
    compute_name: str
    resource_tips: List[str]

    extra_id: str
    extra_data: Optional[Any] = None

    tasks: Optional[List[Task]] = None
    status: JobStatus
    progress: float
    events: Optional[List[Event]] = None
    metrics: Optional[List[Metric]] = None

    org_id: str
    user_id: str
    workspace_id: str

    created_at: datetime
    updated_at: datetime

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


class CreateJobRequest(BaseModel):
    """
    CreateJobRequest is the request to create a job.
    """

    workspace_id: Optional[str] = None
    local_name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None

    kind: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    callback_endpoint: Optional[str] = None
    timeout_in_seconds: Optional[int] = None

    tasks: Optional[list[CreateTaskRequest]] = None

    spec_kind: Optional[SpecKind] = None
    spec_raw: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    filesystem_name: Optional[str] = None
    compute_name: Optional[str] = None
    resource_tips: Optional[List[str]] = None

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


CreateJobResponse: TypeAlias = Job


class JobFilter(BaseModel):
    """
    JobFilter is the filter for jobs
    """

    workspace_id: Optional[str] = None
    local_names: Optional[List[str]] = None
    extra_ids: Optional[List[str]] = None
    kinds: Optional[List[str]] = None
    status: Optional[List[str]] = None
    org_id: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    filter: Optional[str] = None


class ListJobRequest(JobFilter, PagingRequest):
    """
    ListJobRequest is the request to list jobs.
    """

    pass


class ListJobResponse(BaseModel):
    """
    ListJobResponse is the response of listing jobs.
    """

    total_count: int
    result: List[Job]

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


class GetJobRequest(JobName):
    """
    GetJobRequest is the request to get a job.
    """

    has_extra_data: Optional[bool] = False


GetJobResponse: TypeAlias = Job

BatchStopJobRequest: TypeAlias = JobFilter

BatchDeleteJobRequest: TypeAlias = JobFilter

RecreateJobRequest: TypeAlias = JobName


class UpdateJobRequest(JobName):
    """
    UpdateJobRequest is the request to update a job.
    """

    display_name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None


StopJobRequest: TypeAlias = JobName


class DeleteJobRequest(JobName):
    """
    DeleteJobRequest is the request to delete a job.
    """

    force: Optional[bool] = False


class CounterField(BaseModel):
    """
    CounterField is the counter field of the job.
    """

    kinds: List[str]


class CountJobRequest(BaseModel):
    """
    CountJobRequest is the request to count jobs.
    """

    fields: CounterField
    filters: JobFilter


class JobCounter(BaseModel):
    """
    JobCounter is the counter of the job.
    """

    kind: Optional[str] = None
    total_count: int
    pending_count: int
    running_count: int
    succeeded_count: int
    failed_count: int
    terminating_count: int
    terminated_count: int
    partial_succeeded_count: int


class CountJobResponse(JobCounter):
    """
    CountJobResponse is the response of counting jobs.
    """

    kind: List[JobCounter]
