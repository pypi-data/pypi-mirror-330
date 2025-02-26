#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/10/31
# @Author  : zhoubohan
# @File    : job_api_base.py
"""
from enum import Enum


class JobStatus(Enum):
    """
    JobStatus is the status of the job.
    """

    Pending = "Pending"
    Running = "Running"
    Succeeded = "Succeeded"
    Terminating = "Terminating"
    Terminated = "Terminated"
    Failed = "Failed"
    PartialSucceeded = "PartialSucceeded"


def is_finished(status: JobStatus) -> bool:
    """
    Check if job is in a finished state

    Args:
        status: JobStatus enum value

    Returns:
        bool: True if job is finished, False otherwise
    """
    return status in {
        JobStatus.Succeeded,
        JobStatus.PartialSucceeded,
        JobStatus.Terminated,
        JobStatus.Failed,
    }
