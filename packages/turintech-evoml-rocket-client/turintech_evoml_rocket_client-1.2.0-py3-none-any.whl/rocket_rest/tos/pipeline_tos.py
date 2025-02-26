# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import List, Optional

from pydantic import Field

# Core Source imports
from core_common_data_types import CamelCaseBaseModel
from core_common_data_types.base_data_types import CamelCaseModelWithExtra
from core_platform import PlatformType

# Internal libraries
from evoml_api_models import MlTask

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = [
    "PipelineCreationOptionsTo",
    "EvomlIdTo",
    "EvomlToPipelineCreationTo",
    "PipelineCreationTo",
    "PipelineTo",
    "PipelineReportTo",
]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                     Data Models                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class PipelineWheelsOptionsTo(CamelCaseBaseModel):
    """Options to apply in the creation of the pipeline related with the library wheel files"""

    add_wheels: Optional[bool] = Field(
        None, description="Whether to add the wheels of the private libraries to the " "pipeline"
    )
    wheels_architecture: Optional[PlatformType] = Field(
        None, description="Architecture of the machine for which the library must be compatible"
    )


class PipelineCreationOptionsTo(PipelineWheelsOptionsTo):
    """Options to apply in the creation and validation of the pipeline"""

    run_validation: bool = Field(True, description="Whether to validate the pipeline")
    force_project: bool = Field(True, description="Whether to force a new pipeline project")
    force_report: bool = Field(False, description="Whether to force to retrieve a new report from Black Widow")


class EvomlIdTo(CamelCaseBaseModel):
    """Data that identifies an EvoML model"""

    optimization_id: str = Field(..., description="Unique ID of a trial execution", example="d064339028dc478aa2b8f7fa")
    model_id: str = Field(
        ...,
        description="Unique ID a machine learning model created by an specific trial configuration",
        example="894d40f51665951cff3f8800acde9b70703ee24b",
    )


class EvomlToPipelineCreationTo(EvomlIdTo, PipelineCreationOptionsTo):
    """Input data to create a new pipeline of an EvoML model"""


class PipelineCreationTo(CamelCaseBaseModel):
    """Output data of the pipeline creation request"""

    pipeline_id: str = Field(..., description="Unique ID of a pipeline project")
    status: str = Field(..., description="Status value")
    status_details: Optional[str] = Field(None, description="Status details")


class SystemInfoTo(CamelCaseModelWithExtra):
    """Information related with the system needs of the pipeline"""


class PipelineTo(CamelCaseBaseModel):
    """Information about an EvoML pipeline project."""

    pipeline_id: str = Field(..., description="Unique ID that identifies the pipeline")
    system_info: SystemInfoTo = Field(..., description="Information related with the system needs of the pipeline")
    requirements: List[str] = Field([], description="The specific requirements for this model and version")
    status: str = Field(..., description="Status value")
    status_details: Optional[str] = Field(None, description="Status details")
    created_at: str = Field(..., description="Date and time the pipeline was created")
    updated_at: Optional[str] = Field(..., description="Date and time the pipeline was updated")


class PipelineReportTo(CamelCaseBaseModel):
    """Information about an EvoML pipeline project and its final report (Same as ThanosModelReport in Black Widow)"""

    ml_task: MlTask
    pipeline_id: str
    pipeline_zip_file_id: str
    pipeline_handler_file_id: str
