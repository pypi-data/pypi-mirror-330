"""Implements an HTTP client for Rocket API"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Optional, List

from pydantic import parse_obj_as

# Core Source imports
from core_exceptions.core import InvalidParameterException
from core_rest_clients.api_client import ApiClient
from core_pagination.pagination_tos import PaginationTo

# Source imports
from rocket.dtos.pipeline_dtos import EvomlPipelineCreation
from rocket_client.models import CreateOptimizationPipelineTo, OptimizationPipelineTo, PipelinesTo
from rocket_rest.tos.pipeline_tos import PipelineTo, PipelineReportTo, PipelineCreationTo
from rocket_rest.endpoints.router_prefixes import PIPELINE_ROUTER_PREFIX, OPTIMIZATION_ROUTER_PREFIX

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["PipelineClient"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                   Pipeline Client                                                    #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
class PipelineClient(ApiClient):
    """This is a pipeline client implementation for Rocket"""

    # ──────────────────────────── pipelines ───────────────────────────── #

    def get_pipeline(self, pipeline_id: str) -> PipelineTo:
        """Get a pipeline by its ID

        Args:
            pipeline_id (str): The ID of the pipeline to retrieve

        Returns:
            Pipeline: The pipeline
        """
        if not pipeline_id:
            raise InvalidParameterException(message=f"You must specify a valid pipeline_id: '{pipeline_id}'")
        _, response = self.get(f"{PIPELINE_ROUTER_PREFIX}/{pipeline_id}")

        return parse_obj_as(PipelineTo, response)

    def get_pipelines(self, pipelines_to: PipelinesTo = PipelinesTo()) -> PaginationTo[PipelineTo]:
        """Get a list of pipelines by their IDs and status

        Args:
            pipeline_ids (Optional[List[str]], optional): The IDs of the pipelines to retrieve. Defaults to None.
        Returns:
            Pagination[Pipeline]: The list of pipelines
        """
        _, response = self.get(
            PIPELINE_ROUTER_PREFIX,
            params={
                "pipelineIds": pipelines_to.pipeline_ids,
                "status": pipelines_to.status,
                "page": pipelines_to.pagination.page,
                "perPage": pipelines_to.pagination.per_page,
            },
        )

        return parse_obj_as(PaginationTo[PipelineTo], response)

    def get_pipeline_report(self, pipeline_id: str) -> PipelineReportTo:
        """Get the report of a pipeline by its ID

        Args:
            pipeline_id (str): The ID of the pipeline to retrieve

        Returns:
            PipelineReport: The report of the pipeline
        """
        if not pipeline_id:
            raise InvalidParameterException(message=f"You must specify a valid pipeline_id: '{pipeline_id}'")
        _, response = self.get(f"{PIPELINE_ROUTER_PREFIX}/{pipeline_id}/report")

        return parse_obj_as(PipelineReportTo, response)

    def update_pipeline(self, pipeline_id: str, pipeline: PipelineTo) -> PipelineTo:
        """Update a pipeline by its ID

        Args:
            pipeline_id (str): The ID of the pipeline to update
            pipeline (Pipeline): The pipeline to update

        Returns:
            Pipeline: The updated pipeline
        """
        _, response = self.put(f"{PIPELINE_ROUTER_PREFIX}/{pipeline_id}", json=pipeline)

        return parse_obj_as(PipelineTo, response)

    def remove_pipelines(self, pipeline_ids: Optional[List[str]]):
        """Remove a list of pipelines by their IDs

        Args:
            pipeline_ids (Optional[List[str]]): The IDs of the pipelines to remove
        """
        self.delete(PIPELINE_ROUTER_PREFIX, params={"pipelineIds": pipeline_ids})

    def remove_pipeline(self, pipeline_id: str):
        """Remove a pipeline by its ID

        Args:
            pipeline_id (str): The ID of the pipeline to remove
        """
        if not pipeline_id:
            raise InvalidParameterException(message=f"You must specify a valid pipeline_id: '{pipeline_id}'")
        self.delete(f"{PIPELINE_ROUTER_PREFIX}/{pipeline_id}")

    # ──────────────────────────── optimizations ───────────────────────────── #
    def get_optimization_model_pipeline(
        self, optimization_pipeline_to: OptimizationPipelineTo
    ) -> PaginationTo[PipelineTo]:
        """Get a list of pipelines by their IDs and status

        Args:
            optimizayion_pipeline_to (OptimizationPipelineTo): The IDs of the pipelines to retrieve.
        Returns:
            Pagination[Pipeline]: The list of pipelines
        """
        if not optimization_pipeline_to.optimization_id or not optimization_pipeline_to.model_id:
            raise InvalidParameterException(
                message=f"You must specify a valid optimization_id and model_id: '"
                f"{optimization_pipeline_to.optimization_id}' and '{optimization_pipeline_to.model_id}'"
            )
        _, response = self.get(
            f"{OPTIMIZATION_ROUTER_PREFIX}/{optimization_pipeline_to.optimization_id}/models"
            f"/{optimization_pipeline_to.model_id}",
            params={
                "status": optimization_pipeline_to.status,
                "position": optimization_pipeline_to.position,
                "page": optimization_pipeline_to.pagination.page,
                "perPage": optimization_pipeline_to.pagination.per_page,
            },
        )

        return parse_obj_as(PaginationTo[PipelineTo], response)

    def get_optimization_model_pipeline_report(
        self, optimization_pipeline_to: OptimizationPipelineTo
    ) -> PaginationTo[PipelineReportTo]:
        """Get a list of pipelines by their IDs and status

        Args:
            optimization_pipeline_to (OptimizationPipelineTo): The IDs of the pipelines to retrieve.
        Returns:
            Pagination[PipelineReport]: The list of pipelines
        """
        if not optimization_pipeline_to.optimization_id or not optimization_pipeline_to.model_id:
            raise InvalidParameterException(
                message=f"You must specify a valid optimization_id and model_id: '"
                f"{optimization_pipeline_to.optimization_id}' and '{optimization_pipeline_to.model_id}'"
            )
        _, response = self.get(
            f"{OPTIMIZATION_ROUTER_PREFIX}/{optimization_pipeline_to.optimization_id}/models"
            f"/{optimization_pipeline_to.model_id}/report",
            params={
                "status": optimization_pipeline_to.status,
                "position": optimization_pipeline_to.position,
                "page": optimization_pipeline_to.pagination.page,
                "perPage": optimization_pipeline_to.pagination.per_page,
            },
        )

        return parse_obj_as(PaginationTo[PipelineReportTo], response)

    def create_optimization_model_pipelines(
        self, evoml_pipelines: List[EvomlPipelineCreation]
    ) -> PaginationTo[PipelineCreationTo]:
        """Create and validate a EvoML pipeline project for each ML Model configuration of the list.

        Args:
            evoml_pipelines (List[EvomlPipelineCreation]): The list of data that
            identifies the EvoML models for which to create the pipeline
        Returns:
            Pagination[PipelineCreation]: The list of created pipelines
        """
        _, response = self.post(OPTIMIZATION_ROUTER_PREFIX, json=evoml_pipelines)

        return parse_obj_as(PaginationTo[PipelineCreationTo], response)

    def create_optimization_model_pipeline(
        self, create_optimization_pipeline_to: CreateOptimizationPipelineTo
    ) -> PipelineCreationTo:
        """Create and validate a EvoML pipeline project for a ML Model configuration

        Args:
            create_optimization_pipeline_to (CreateOptimizationPipelineTo): The data that identifies the EvoML model
        Returns:
            PipelineCreation: The created pipeline
        """
        if not create_optimization_pipeline_to.optimization_id or not create_optimization_pipeline_to.model_id:
            raise InvalidParameterException(
                message=f"You must specify a valid optimization_id and model_id: '"
                f"{create_optimization_pipeline_to.optimization_id}'-'{create_optimization_pipeline_to.model_id}'"
            )
        _, response = self.post(
            f"{OPTIMIZATION_ROUTER_PREFIX}/{create_optimization_pipeline_to.optimization_id}/models"
            f"/{create_optimization_pipeline_to.model_id}",
            json={
                "run_validation": create_optimization_pipeline_to.options.run_validation,
                "force_project": create_optimization_pipeline_to.options.force_project,
                "force_report": create_optimization_pipeline_to.options.force_report,
                "add_wheels": create_optimization_pipeline_to.options.add_wheels,
                "wheels_architecture": create_optimization_pipeline_to.options.wheels_architecture,
            },
        )

        return parse_obj_as(PipelineCreationTo, response)
