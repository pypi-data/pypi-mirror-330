# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Optional, List

from pydantic import BaseModel, Field

# Core Source imports
from core_common_dtos.common_dtos import StatusInfo
from core_utils.hash_utils import compose_hash_id

# Source imports
from rocket.data_types.environment_types import EnvironmentStatus

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = [
    "EnvironmentId",
    "EnvironmentSpecificationsDto",
    "EnvironmentDto",
    "EnvironmentCreationDto",
    "EnvironmentRegistrationDto",
    "EnvironmentCreationDto",
]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      DTO Models                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class EnvironmentId(BaseModel):
    """Information of an environment"""

    id: str = Field(..., description="Unique ID that identifies the environment")

    @property
    def data_id(self) -> "EnvironmentId":
        return EnvironmentId(**self.dict())


class EnvironmentSpecificationsDto(BaseModel):
    """Information that defines an environment"""

    # pylint: disable=R0801
    python_version: str = Field(..., description="The version of the python which the environment will have")
    pip_version: Optional[str] = Field(None, description="THe version of the pip that the environment will have")
    ray_version: str = Field(..., description="The version of Ray")
    requirements: List[str] = Field([], description="The specific requirements of the environment")
    channels: Optional[List[str]] = Field(None, description="Refer to channels to download the packages")
    dependencies: Optional[List[str]] = Field(
        None, description="Such as the libraries you wish to pre-install when creating the environment"
    )

    @property
    def hash_id(self) -> str:
        # Get the dict of values
        values_dict = self.dict()
        # Sort the list data in the dictionary
        self.sort_data_lists(values_dict)
        return compose_hash_id(values=list(values_dict.values()))

    @property
    def specifications(self) -> "EnvironmentSpecificationsDto":
        return EnvironmentSpecificationsDto(**self.dict())

    @staticmethod
    def sort_data_lists(data: dict):
        lists_to_sort = ["requirements", "channels", "dependencies"]
        # Sort the necessary lists
        for list_name in lists_to_sort:
            if data.get(list_name):
                data[list_name] = sorted(data[list_name])


class EnvironmentStatusInfo(StatusInfo[EnvironmentStatus]):
    """Information about the environment generation and creation process status"""

    status: EnvironmentStatus


class EnvironmentDto(EnvironmentId):
    """Information of an environment"""

    specifications: EnvironmentSpecificationsDto = Field(..., description="Information that defines an environment.")
    state: EnvironmentStatusInfo = Field(..., description="Status of the environment")

    @property
    def status(self) -> str:
        return self.state.status.value

    @property
    def status_details(self) -> Optional[str]:
        return self.state.status_details

    @property
    def is_created(self) -> bool:
        return EnvironmentStatus.CREATED.is_status(self.status)

    @property
    def is_failed(self) -> bool:
        return EnvironmentStatus.FAILED.is_status(self.status)

    @property
    def is_done(self) -> bool:
        return self.state.status in [EnvironmentStatus.CREATED, EnvironmentStatus.FAILED]

    def __init__(
        self,
        specifications: EnvironmentSpecificationsDto,
        environment_id: Optional[EnvironmentId] = None,
        **kwargs,
    ):
        if environment_id:
            kwargs.update(environment_id.dict())
        if not kwargs.get("id"):
            kwargs["id"] = specifications.hash_id
        kwargs["specifications"] = specifications
        super().__init__(**kwargs)


class EnvironmentRegistrationDto(BaseModel):
    """Information needed to register a new environment."""

    specifications: EnvironmentSpecificationsDto = Field(..., description="Information that defines an environment.")
    id: Optional[str] = Field(None, description="Unique ID that identifies the environment")


class EnvironmentCreationDto(EnvironmentRegistrationDto):
    """Information needed to create a new environment."""

    create: Optional[bool] = Field(
        True, description="Flag indicating whether to create the environment (True) or just register it (False)"
    )
