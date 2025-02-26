# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Optional

from pydantic import Field

# Core Source imports
from core_common_data_types import CamelCaseBaseModel

# Source imports
from rocket.dtos.environment_dtos import EnvironmentSpecificationsDto

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["EnvironmentTo", "EnvironmentCreationTo"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                     Data Models                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class EnvironmentTo(CamelCaseBaseModel):
    """Information of an environment"""

    environment_id: str = Field(..., description="Unique ID that identifies the environment")
    status: str = Field(..., description="Status value")
    status_details: Optional[str] = Field(None, description="Status details")


class EnvironmentCreationTo(CamelCaseBaseModel, EnvironmentSpecificationsDto):
    """Information of an environment creation process"""

    create: Optional[bool] = Field(
        False, description="Flag indicating whether to create the environment (True) or just register it (False)"
    )
