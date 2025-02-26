#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/10/31
# @Author  : zhoubohan
# @File    : job_api_event.py
"""
import re
from datetime import datetime
from enum import Enum
from typing import Optional, Union, TypeAlias

from bceinternalsdk.client.base_model import BaseModel
from bceinternalsdk.client.paging import PagingRequest

job_event_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/jobs/(?P<job_name>.+?)"
    "/events/(?P<local_name>.+?)$"
)

task_event_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/jobs/(?P<job_name>.+?)"
    "/tasks/(?P<task_name>.+?)/events/(?P<local_name>.+?)$"
)


class EventKind(Enum):
    """
    EventKind is the kind of the event.
    """

    Normal = "Normal"
    Succeed = "Succeeded"
    Failed = "Failed"


class JobEventName(BaseModel):
    """
    JobEventName is the unique identifier for a JobEvent.
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
        Get the name of the JobEvent.
        :return: str
        """
        return f"workspaces/{self.workspace_id}/jobs/{self.job_name}/events/{self.local_name}"


class TaskEventName(BaseModel):
    """
    TaskEventName is the unique identifier for a TaskEvent.
    """

    workspace_id: str
    job_name: str
    task_name: str
    local_name: str

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True

    def get_name(self):
        """
        Get the name of the TaskEvent.
        :return: str
        """
        return f"workspaces/{self.workspace_id}/jobs/{self.job_name}/tasks/{self.task_name}/events/{self.local_name}"


def parse_event_name(name: str) -> Optional[Union[JobEventName, TaskEventName]]:
    """
    Parse the event name to JobEventName or TaskEventName.
    :param name: str
    :return: Optional[JobEventName, TaskEventName]
    """
    task_match = task_event_name_regex.match(name)
    if task_match:
        return TaskEventName(**task_match.groupdict())

    job_match = job_event_name_regex.match(name)
    if job_match:
        return JobEventName(**job_match.groupdict())

    return None


class CreateEventRequest(BaseModel):
    """
    CreateEventRequest is the request for creating an event.
    """

    workspace_id: Optional[str] = None
    job_name: Optional[str] = None
    task_name: Optional[str] = None
    kind: Optional[EventKind] = EventKind.Normal
    reason: str
    message: str

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True

    def get_job_name(self):
        """
        Get the name of the job.
        :return: str
        """
        return f"workspaces/{self.workspace_id}/jobs/{self.job_name}"


class Event(BaseModel):
    """
    Event is the event of a job or a task.
    """

    id: str
    kind: EventKind
    reason: str
    message: str
    workspace_id: str
    job_name: str
    task_name: str
    created_at: datetime
    updated_at: datetime

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


CreateEventResponse: TypeAlias = Event


class EventFilter(BaseModel):
    """
    EventFilter is the filter for events.
    """

    workspace_id: str
    job_name: str
    task_name: Optional[str] = None
    kinds: Optional[list[EventKind]] = None

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


class ListEventRequest(EventFilter, PagingRequest):
    """
    ListEventRequest is the request to list events.
    """

    pass


class ListEventResponse(BaseModel):
    """
    ListEventResponse is the response of listing events.
    """

    total_count: int
    result: list[Event]

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True
