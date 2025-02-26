# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Optional

from pydantic import Field

# Core Source imports
from core_common_data_types import CamelCaseBaseModel

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["EvomlDependencyTo", "PipelineVersionTO"]

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                     Data Models                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class EvomlDependencyTo(CamelCaseBaseModel):
    """Data that identifies an Evoml dependency set"""

    metaml_version: str = Field(..., example="1.0.0", description="The version of metaml")
    preprocessor_version: str = Field(..., example="1.0.0", description="The version of preprocessor")
    pipeline_version: str = Field(..., example="1.0.0", description="The version of the pipeline")
    utils_version: str = Field(
        example="1.0.0", description="The version of evoml-utils (transitive dependency of preprocessor)"
    )
    models_version: str = Field(description="The version of evoml-api-models (transitive dependency of preprocessor)")
    offline_environment: Optional[str] = Field(
        None, example="pipeline_management_evoml_1.0.0", description="The name or conda env already created"
    )


class PipelineVersionTO(CamelCaseBaseModel):
    """Data holding the version of pipeline generation internal libraries"""

    pipeline_version: str = Field(..., example="1.0.0", description="The version of the pipeline")
