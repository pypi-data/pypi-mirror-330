# pylint: disable=no-self-argument
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Optional, Dict, List, Tuple
from uuid import UUID, uuid4

from pydantic import Field, BaseModel, validator

# Core Source imports
from core_common_data_types.type_definitions import PositionType
from core_common_dtos.common_dtos import StatusInfo, ModelId, DateTimeInfo, CreatedAt
from core_exceptions.core import InvalidParameterException
from core_utils.validators import validate_enum_name

# Source imports
from rocket.data_types.pipeline_types import PipelineStatus, PipelineTaskType, PipelineProcessType
from rocket.dtos.evoml_dtos import EvomlId, EstimatorInfo, EvomlModelInfo, BaseEvomlId
from rocket.dtos.library_dtos import LibraryInfo
from rocket.dtos.system_dtos import SystemInfo

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = [
    "PipelineWheelsOptions",
    "PipelineCreationOptions",
    "EvomlPipelineCreation",
    "PipelineUpdate",
    "PipelineDataFiles",
    "PipelineReportId",
    "PipelineReport",
    "PipelineStatusInfo",
    "PipelineId",
    "Pipeline",
    "PipelineInfo",
    "PipelineFilters",
    "PipelineTaskId",
    "PipelineTask",
    "PipelineProcess",
]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      DTO Models                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


# --------------------------------------- Pipeline Report ---------------------------------------- #


class PipelineDataFiles(BaseModel):
    """The IDs and extra information of the files that make up the pipeline data directory."""

    pipeline_data_id: str = Field(
        ..., description="ID of the pipeline data files generated in Black Widow and stored in Thor"
    )
    sample_file_id: str = Field(..., description="ID of the dataset sample file used in the preprocessor")
    model_joblib: EstimatorInfo = Field(
        ..., description="Object that contains the info about the estimator produced for a model"
    )
    preprocessor_appendix: EstimatorInfo = Field(
        ..., description="Object that contains the info about the estimator produced for a preprocessor"
    )

    @property
    def wheels_requirements(self) -> Tuple[List[str], List[LibraryInfo]]:
        """Tuple of lists of public/private requirements needed for the files of this pipeline"""
        return ["scikit-learn==1.1.3"], [self.model_joblib.library, self.preprocessor_appendix.library]

    @property
    def requirements(self) -> List[str]:
        """List of requirements needed for the files of this pipeline"""
        public_req, private_req = self.wheels_requirements
        return public_req + [req.dependency for req in private_req]


class PipelineReportId(ModelId["PipelineReportId"]):
    """Data that identifies a final model report of a pipeline model optimization"""


class PipelineReport(PipelineReportId, BaseEvomlId):
    """Final model report of a pipeline model optimization"""

    model_info: EvomlModelInfo = Field(..., description="General information about the EvoML model.")
    data_files: PipelineDataFiles = Field(
        ..., description="The IDs and extra information of the files that make up the pipeline data directory."
    )


# --------------------------------------- Pipeline Status ---------------------------------------- #


class PipelineStatusInfo(StatusInfo[PipelineStatus]):
    """Information about the pipeline generation and creation process status"""

    status: PipelineStatus


# ------------------------------------------- Pipeline ------------------------------------------- #


class PipelineId(ModelId["PipelineId"]):
    """Data that identifies an EvoML pipeline project."""


class Pipeline(PipelineId, BaseEvomlId, DateTimeInfo):
    """Information about an EvoML pipeline project."""

    report_id: Optional[str] = Field(None, description="Unique ID of a pipeline report")
    template: Optional[Dict] = Field(None, description="Configuration attributes of the Pipeline Template")
    thor_file_id: Optional[str] = Field(None, description="Thor ID of the pipeline.zip file")
    thor_handler_file_id: Optional[str] = Field(None, description="Thor ID of the pipeline_handler.py file")
    system_info: SystemInfo = Field(..., description="Information related with the system needs of the pipeline")
    state: PipelineStatusInfo = Field(..., description="Status of the pipeline project")
    requirements: List[str] = Field([], description="The specific requirements for this model and version")

    @property
    def report_data_id(self) -> PipelineReportId:
        if self.report_id:
            return PipelineReportId(uuid=self.report_id)
        raise InvalidParameterException(message="Pipeline without associated report")

    @property
    def status(self) -> str:
        return self.state.status.value

    @property
    def status_details(self) -> Optional[str]:
        return self.state.status_details

    @property
    def is_pending(self) -> bool:
        return self.state.status is PipelineStatus.PENDING

    @property
    def is_created(self) -> bool:
        return self.state.status in [
            PipelineStatus.CREATED,
            PipelineStatus.VALIDATED,
            PipelineStatus.FAILED,
            PipelineStatus.UPLOADED,
        ]

    @property
    def is_validated(self) -> bool:
        return self.state.status in [PipelineStatus.VALIDATED, PipelineStatus.FAILED]

    @property
    def is_failed(self) -> bool:
        return self.state.status is PipelineStatus.FAILED


class PipelineInfo(BaseModel):
    """Full information about the Pipeline"""

    pipeline: Pipeline = Field(..., description="Information about an EvoML pipeline project.")
    report: PipelineReport = Field(..., description="Final model report of a pipeline model optimization")


class PipelineFilters(BaseModel):
    """Filters to apply when search a pipeline"""

    pipeline_ids: Optional[List[PipelineId]] = Field(None, description="List of pipeline IDs to retrieve.")
    evoml_id: Optional[EvomlId] = Field(
        None, description="EvomlId filter. Keeps pipeline that matches optimisation id and model id."
    )
    status: Optional[PipelineStatus] = Field(
        None, description="Pipline status filter. Keeps pipelines that match the status."
    )
    position: Optional[PositionType] = Field(
        None, description="Pipeline position filter. Keeps oldest or latest pipeline."
    )
    only_with_zip: Optional[bool] = Field(
        None, description="Retrieve only those pipelines that have a pipeline.zip file ID."
    )


# -------------------------------------- Pipeline Creation --------------------------------------- #


class PipelineWheelsOptions(BaseModel):
    """Options to apply in the creation of the pipeline related with the library wheel files"""

    add_wheels: Optional[bool] = Field(
        None, description="Whether to add the wheels of the private libraries to the " "pipeline"
    )
    # Because of `offline_environment` we can't add core-platform dependencies here (this model is used in
    # PipelineActor, so it throws `ModuleNotFoundError: No module named 'core_platform'`).
    # Old core dependencies are not compatible with this new library
    wheels_architecture: Optional[str] = Field(  # PlatformType
        None, description="Architecture of the machine for which the library must be compatible"
    )


class PipelineCreationOptions(PipelineWheelsOptions):
    """Options to apply in the creation and validation of the pipeline"""

    run_validation: bool = Field(..., description="Whether to validate the pipeline")
    force_project: bool = Field(..., description="Whether to force a new pipeline project")
    force_report: bool = Field(..., description="Whether to force to retrieve a new report from Black Widow")


class EvomlPipelineCreation(PipelineCreationOptions):
    """Input data to create a new pipeline of an EvoML model"""

    evoml_id: EvomlId = Field(..., description="Data that identifies an EvoML optimization model")


class PipelineUpdate(PipelineCreationOptions):
    """Input data to update a pipeline of an EvoML model"""

    pipeline_id: PipelineId = Field(..., description="Data that identifies an EvoML pipeline project")


# --------------------------------------- Pipeline Process --------------------------------------- #


class PipelineTaskId(ModelId["PipelineTaskId"]):
    """Data that identifies a pipeline task."""

    uuid: UUID = Field(default_factory=uuid4, description="Unique ID")


class PipelineTask(PipelineTaskId, DateTimeInfo):
    """Information of a task involve into a pipeline process"""

    task_type: PipelineTaskType = Field(..., description="Type of task")
    status: PipelineStatus = Field(PipelineStatus.PENDING, description="Pipeline task status")

    # Validators
    _validate_task_type = validator("task_type", pre=True)(
        lambda value: validate_enum_name(value=value, type_=PipelineTaskType)
    )


class PipelineProcessId(ModelId["PipelineProcessId"]):
    """Data that identifies a pipeline process."""

    uuid: UUID = Field(default_factory=uuid4, description="Unique ID")


class PipelineProcess(PipelineProcessId, CreatedAt):
    """Information about a pipeline process"""

    pipeline_id: str = Field(..., description="Data that identifies an EvoML pipeline project")
    process_type: PipelineProcessType = Field(..., description="Type of process of a pipeline")
    tasks: Dict[PipelineTaskType, PipelineTask] = Field({}, description="List of tasks involve in the pipeline process")

    # Validators
    _validate_process_type = validator("process_type", pre=True)(
        lambda value: validate_enum_name(value=value, type_=PipelineProcessType)
    )

    @property
    def tasks_list(self) -> List[PipelineTask]:
        return [self.tasks[task_type] for task_type in self.process_type.value if task_type in self.tasks]
