#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/10/31
# @Author  : zhoubohan
# @File    : job_api_task.py
"""
import re
from datetime import datetime
from typing import Optional, List, TypeAlias

from bceinternalsdk.client.base_model import BaseModel
from bceinternalsdk.client.paging import PagingRequest

from .job_api_base import JobStatus
from .job_api_event import Event
from .job_api_metric import Metric

task_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/jobs/(?P<job_name>.+?)"
    "/tasks/(?P<local_name>.+?)$"
)


class TaskName(BaseModel):
    """
    TaskName is the unique identifier for a Task.
    """

    workspace_id: str
    job_name: str
    local_name: str

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True

    def get_name(self):
        """
        Get the name of the Task.
        :return: str
        """
        return (
            f"workspaces/{self.workspace_id}/jobs/{self.job_name}/"
            f"tasks/{self.local_name}"
        )


def parse_task_name(name: str) -> Optional[TaskName]:
    """
    Parse the TaskName from the name string.
    :param name: str
    :return: Optional[TaskName]
    """
    match = task_name_regex.match(name)
    if match:
        return TaskName(**match.groupdict())
    return None


class Task(BaseModel):
    """
    Task is the model of the task.
    """

    name: str
    local_name: str
    display_name: str
    description: str
    kind: str
    order: int
    status: JobStatus
    progress: float
    events: Optional[List[Event]] = None
    metrics: Optional[List[Metric]] = None
    org_id: str
    user_id: str
    workspace_id: str
    job_name: str
    created_at: datetime
    updated_at: datetime

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


class CreateTaskRequest(BaseModel):
    """
    CreateTaskRequest is the request for creating a new Task.
    """

    workspace_id: Optional[str] = None
    job_name: Optional[str] = None
    local_name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    kind: Optional[str] = None
    order: Optional[int] = 0

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


CreateTaskResponse: TypeAlias = Task


class TaskFilter(BaseModel):
    """
    TaskFilter is the filter for tasks.
    """

    workspace_id: str
    job_name: str
    kinds: Optional[List[str]] = None
    status: Optional[List[JobStatus]] = None
    filter: Optional[str] = None

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


class ListTaskRequest(TaskFilter, PagingRequest):
    """
    ListTaskRequest is the request for listing tasks.
    """

    pass


class ListTaskResponse(BaseModel):
    """
    ListTaskResponse is the response of listing tasks.
    """

    total_count: int
    result: List[Task]

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


GetTaskRequest: TypeAlias = TaskName

GetTaskResponse: TypeAlias = Task


class UpdateTaskRequest(TaskName):
    """
    UpdateTaskRequest is the request for updating a task.
    """

    display_name: Optional[str] = None
    description: Optional[str] = None


DeleteTaskRequest: TypeAlias = TaskName

StopTaskRequest: TypeAlias = TaskName
