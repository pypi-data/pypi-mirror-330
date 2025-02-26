# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Optional, List

from pydantic import BaseModel

from core_common_data_types.type_definitions import PositionType
from core_pagination.pagination_tos import PaginationQueryParams
from rocket.data_types.pipeline_types import PipelineStatus
from rocket_rest.tos.pipeline_tos import PipelineCreationOptionsTo, EvomlIdTo

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["OptimizationPipelineTo", "CreateOptimizationPipelineTo", "PipelinesTo", "EnvironmentsTo"]

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                       Rocket Client Rest Models                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class OptimizationPipelineTo(EvomlIdTo):
    """Optimization Pipeline Transfer Object"""

    status: Optional[PipelineStatus] = None
    position: Optional[PositionType] = None
    pagination: PaginationQueryParams = PaginationQueryParams()


class CreateOptimizationPipelineTo(EvomlIdTo):
    """Create Optimization Pipeline Transfer Object"""

    options: PipelineCreationOptionsTo = PipelineCreationOptionsTo()


class PipelinesTo(BaseModel):
    """Pipelines Transfer Object"""

    pipeline_ids: Optional[List[str]] = None
    status: Optional[PipelineStatus] = None
    pagination: PaginationQueryParams = PaginationQueryParams()


class EnvironmentsTo(BaseModel):
    """Environments Transfer Object"""

    environment_ids: Optional[List[str]] = None
    created: bool = True
    pagination: PaginationQueryParams = PaginationQueryParams()
