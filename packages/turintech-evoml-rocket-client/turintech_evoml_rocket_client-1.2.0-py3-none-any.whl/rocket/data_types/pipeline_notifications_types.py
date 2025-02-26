# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Dict

# Source imports
from rocket.clients.data_types.loki_types import ExecutionStatus
from rocket.data_types.pipeline_types import PipelineStatus

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["PIPELINE_EXECUTION_STATUS"]

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      Data types                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

PIPELINE_EXECUTION_STATUS: Dict[PipelineStatus, ExecutionStatus] = {
    PipelineStatus.PENDING: ExecutionStatus.CREATED,
    PipelineStatus.IN_CREATION: ExecutionStatus.RUNNING,
    PipelineStatus.IN_PROGRESS: ExecutionStatus.RUNNING,
    PipelineStatus.IN_VALIDATION: ExecutionStatus.RUNNING,
    PipelineStatus.CREATED: ExecutionStatus.SUCCESS,
    PipelineStatus.VALIDATED: ExecutionStatus.SUCCESS,
    PipelineStatus.UPLOADED: ExecutionStatus.SUCCESS,
    PipelineStatus.FAILED: ExecutionStatus.FAILED,
}
"""Mapping between the status value of a pipeline and the status value of notifications."""
