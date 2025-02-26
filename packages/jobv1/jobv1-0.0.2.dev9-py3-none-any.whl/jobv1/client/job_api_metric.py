#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/10/31
# @Author  : zhoubohan
# @File    : job_api_metric.py
"""
import re
from datetime import datetime
from enum import Enum
from typing import List, Optional, TypeAlias

from bceinternalsdk.client.base_model import BaseModel
from bceinternalsdk.client.paging import PagingRequest

job_metric_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/jobs/(?P<job_name>.+?)"
    "/metrics/(?P<local_name>.+?)$"
)

task_metric_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/jobs/(?P<job_name>.+?)"
    "/tasks/(?P<task_name>.+?)/metrics/(?P<local_name>.+?)$"
)


class MetricKind(Enum):
    """
    Kind is the kind of the metric.
    """

    Counter = "Counter"
    Gauge = "Gauge"


class CounterKind(Enum):
    """
    CounterKind is the kind of the counter metric.
    """

    Monotonic = "Monotonic"
    Cumulative = "Cumulative"


class DataType(Enum):
    """
    DataType is the data type of the metric.
    """

    Int = "Int"
    Float = "Float"
    String = "String"


class MetricLocalName(Enum):
    """
    MetricLocalName is the local name of the metric.
    """

    Status = "status"
    Total = "total"
    Success = "success"
    Failed = "failed"


class MetricName(BaseModel):
    """
    MetricName is the unique identifier for a Metric.
    """

    workspace_id: str
    job_name: str
    task_name: Optional[str] = None
    local_name: str

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True

    def get_name(self):
        """
        Get the name of the Metric.
        :return: str
        """
        if self.task_name is not None and len(self.task_name) > 0:
            return (
                f"workspaces/{self.workspace_id}/jobs/{self.job_name}/tasks/{self.task_name}/"
                f"metrics/{self.local_name}"
            )

        return f"workspaces/{self.workspace_id}/jobs/{self.job_name}/metrics/{self.local_name}"


class Metric(BaseModel):
    """
    Metric is the model of the metric.
    """

    name: str
    local_name: str
    display_name: str
    description: str
    kind: MetricKind
    counter_kind: CounterKind
    value: List[str]
    data_type: DataType
    workspace_id: str
    job_name: str
    task_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


class CreateMetricRequest(BaseModel):
    """
    CreateMetricRequest is the request for creating a metric.
    """

    workspace_id: Optional[str] = None
    job_name: Optional[str] = None
    task_name: Optional[str] = None
    local_name: MetricLocalName
    display_name: Optional[str] = None
    description: Optional[str] = None
    kind: MetricKind = MetricKind.Counter
    counter_kind: CounterKind = CounterKind.Cumulative
    value: Optional[List[str]] = None
    data_type: DataType = DataType.Int

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


CreateMetricResponse: TypeAlias = Metric


class ListMetricRequest(PagingRequest):
    """
    ListMetricRequest is the request for listing metrics.
    """

    workspace_id: str
    job_name: str
    task_name: Optional[str] = None

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


class ListMetricResponse(BaseModel):
    """
    ListMetricResponse is the response for listing metrics.
    """

    total_count: int
    result: List[Metric]

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


GetMetricRequest: TypeAlias = MetricName

GetMetricResponse: TypeAlias = Metric


class UpdateMetricRequest(MetricName):
    """
    UpdateMetricRequest is the request for updating a metric.
    """

    display_name: Optional[str] = None
    description: Optional[str] = None


DeleteMetricRequest: TypeAlias = MetricName
