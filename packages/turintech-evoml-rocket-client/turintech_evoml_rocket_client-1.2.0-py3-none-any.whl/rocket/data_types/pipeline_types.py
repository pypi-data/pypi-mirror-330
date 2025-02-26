# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from enum import Enum
from typing import List

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["PipelineStatus", "PipelineTaskType", "PipelineProcessType"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      Data types                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class PipelineStatus(str, Enum):
    """Pipeline process and task status"""

    PENDING = "PENDING"
    IN_PROGRESS = "IN PROGRESS"
    IN_CREATION = "IN CREATION"
    UPLOADED = "UPLOADED"
    CREATED = "CREATED"
    IN_VALIDATION = "IN VALIDATION"
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"


class PipelineTaskType(str, Enum):
    """Types of tasks associated with a pipeline"""

    CREATION = "creation"
    VALIDATION = "validation"


class PipelineProcessType(Enum):
    """Types of pipeline process"""

    CREATION = [PipelineTaskType.CREATION]
    VALIDATION = [PipelineTaskType.VALIDATION]
    CREATION_VALIDATION = [PipelineTaskType.CREATION, PipelineTaskType.VALIDATION]
    NOTHING: List[PipelineTaskType] = []
