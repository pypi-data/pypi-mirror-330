"""Implements an HTTP client for Rocket API"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Optional, List

from pydantic import parse_obj_as

# Core Source imports
from core_exceptions.core import InvalidParameterException
from core_rest_clients.api_client import ApiClient
from core_pagination.pagination_tos import PaginationTo

# Source imports
from rocket_client.models import EnvironmentsTo
from rocket_rest.endpoints.router_prefixes import ENVIRONMENT_ROUTER_PREFIX
from rocket_rest.tos.environment_tos import EnvironmentTo, EnvironmentCreationTo

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["EnvironmentClient"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Environment Client                                                    #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
class EnvironmentClient(ApiClient):
    """This is a environmnent client implementation for Rocket"""

    # ──────────────────────────── environments ───────────────────────────── #
    def get_environment(self, environment_id: str) -> EnvironmentTo:
        """Get an environment by its ID.

        Args:
            environment_id (str): The ID of the environment to retrieve
        Returns:
            Environment: The environment
        """
        if not environment_id:
            raise InvalidParameterException(message=f"You must specify a valid environment_id: '{environment_id}'")
        _, response = self.get(f"{ENVIRONMENT_ROUTER_PREFIX}/{environment_id}")

        return parse_obj_as(EnvironmentTo, response)

    def get_environments(self, environments_to: EnvironmentsTo = EnvironmentsTo()) -> PaginationTo[EnvironmentTo]:
        """Get a list of environments by their IDs and creation status.

        Args:
            environments_to (EnvironmentsTo, optional): The IDs of the environments to retrieve. Defaults to None.
        Returns:
            Pagination: The list of environments
        """
        _, response = self.get(
            ENVIRONMENT_ROUTER_PREFIX,
            params={
                "environmentIds": environments_to.environment_ids,
                "created": environments_to.created,
                "page": environments_to.pagination.page,
                "perPage": environments_to.pagination.per_page,
            },
        )

        return parse_obj_as(PaginationTo[EnvironmentTo], response)

    def remove_environments(self, environment_ids: Optional[List[str]]):
        """Remove a list of environments by their IDs.

        Args:
            environment_ids (Optional[List[str]]): The IDs of the environments to remove
        """
        self.delete(ENVIRONMENT_ROUTER_PREFIX, params={"environmentIds": environment_ids})

    def remove_environment(self, environment_id: str):
        """Remove an environment by its ID.

        Args:
            environment_id (str): The ID of the environment to remove
        """
        if not environment_id:
            raise InvalidParameterException(message=f"You must specify a valid environment_id: '{environment_id}'")
        self.delete(f"{ENVIRONMENT_ROUTER_PREFIX}/{environment_id}")

    def create_environments(self, environments_creation: List[EnvironmentCreationTo]) -> List[EnvironmentTo]:
        """Create a list of environments.

        Args:
            environments_creation (List[EnvironmentCreation]): The list of environments to create

        Returns:
            List[Environment]: The list of created environments
        """
        _, response = self.post(ENVIRONMENT_ROUTER_PREFIX, json=environments_creation)
        return parse_obj_as(List[EnvironmentTo], response)

    def create_environment(self, environment_id: str) -> EnvironmentTo:
        """Create an environment by its ID.

        Args:
            environment_id (str): The ID of the environment to create

        Returns:
            Environment: The created environment
        """
        if not environment_id:
            raise InvalidParameterException(message=f"You must specify a valid environment_id: '{environment_id}'")
        _, response = self.post(f"{ENVIRONMENT_ROUTER_PREFIX}/{environment_id}")

        return parse_obj_as(EnvironmentTo, response)
