# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Optional, List

from pydantic import BaseModel, Field

# Core Source imports
from core_common_data_types.base_data_types_dtos import UpdateBaseModel

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


__all__ = [
    "EvomlDependency",
    "EvomlDependencyId",
    "EvomlDependencyFilters",
    "EvomlDependencyCreate",
    "EvomlDependencyUpdate",
]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      DTO Models                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


# ------------------------------------------- Evoml Dependency ------------------------------------------------------- #


class EvomlDependencyId(BaseModel):
    """Data with id that identifies a set of evoml related dependencies"""

    metaml_version: str = Field(description="Version of metaml")
    preprocessor_version: str = Field(description="Version of preprocessor")

    @property
    def data_id(self) -> "EvomlDependencyId":
        return EvomlDependencyId(**self.dict())


class EvomlDependencyData(BaseModel):
    """Data about dependencies"""

    pipeline_version: str = Field(description="Version of pipeline")
    utils_version: str = Field(description="The version of evoml-utils (transitive dependency of preprocessor)")
    models_version: str = Field(description="The version of evoml-api-models (transitive dependency of preprocessor)")
    offline_environment: Optional[str] = Field(
        default=None, description="Name of pre-created environment for offline usage"
    )


class EvomlDependencyCreate(EvomlDependencyId, EvomlDependencyData):
    """Creation form for a set of evoml related dependencies"""


class EvomlDependency(EvomlDependencyCreate):
    """Data about a set of evoml related dependencies"""

    id: str = Field(description="Unique id that identifies the set of evoml related dependencies")


class EvomlDependencyUpdate(EvomlDependencyData, UpdateBaseModel):
    """Update a set of EvoML related dependencies"""


class EvomlDependencyFilters(BaseModel):
    """Filters to apply when searching for a set of evoml dependencies"""

    ids: Optional[List[str]] = Field(
        None, description="List of unique IDs that identifies the set of evoml related dependencies"
    )
    evoml_dependency_ids: Optional[List[EvomlDependencyId]] = Field(
        None, description="Data that identifies the evoml dependency set"
    )
