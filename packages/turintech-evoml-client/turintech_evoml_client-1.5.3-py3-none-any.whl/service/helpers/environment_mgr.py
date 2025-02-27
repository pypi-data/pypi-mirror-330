# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Optional, List

# Core Source imports
from core_rest_clients.api_client_conf import ApiClientConf
from core_pagination.pagination_tos import PaginationTo, PaginationQueryParams

# Source imports
from rocket_rest.tos.environment_tos import EnvironmentTo, EnvironmentCreationTo
from rocket_client.environment_client import EnvironmentClient
from rocket_client.models import EnvironmentsTo
from evoml_client.api_calls import get_url, get_auth

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["EnvironmentHelper"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                   Environment Helper                                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
class EnvironmentHelper:
    """This is an environment helper implementation for Rocket"""

    def __init__(self, env: str):
        """Initialize the environment helper"""
        self.rocket_client = EnvironmentClient(
            ApiClientConf(
                protocol=None,
                host=get_url("rocket"),
                port=None,
                postfix=None,
                headers=get_auth(),
            )
        )

    def get_all_environments(
        self, environment_ids: Optional[List[str]] = None, created: bool = True, page: int = 1, per_page: int = 10
    ) -> PaginationTo[EnvironmentTo]:
        """Get a list of environments by their IDs and creation status

        Args:
            environment_ids (Optional[List[str]], optional): The IDs of the environments to retrieve.Defaults to None.
            created (bool, optional): The creation status of the environments to retrieve. Defaults to True.
            page (int, optional): The page number. Defaults to 1.
            per_page (int, optional): The number of items per page. Defaults to 10.

        Returns:
            Pagination: The list of environments
        """
        return self.rocket_client.get_environments(
            EnvironmentsTo(
                pipeline_ids=environment_ids,
                status=created,
                pagination=PaginationQueryParams(page=page, per_page=per_page),
            )
        )

    def get_environment_by_id(self, environment_id: str) -> EnvironmentTo:
        """Get an environment by its ID

        Args:
            environment_id (str): The ID of the environment to retrieve
        Returns:
            Environment: The environment
        """
        return self.rocket_client.get_environment(environment_id)

    def remove_environments(self, environment_ids: Optional[List[str]]):
        """Remove a list of environments by their IDs

        Args:
            environment_ids (Optional[List[str]]): The IDs of the environments to remove
        Returns:
            Environment: The environment
        """
        return self.rocket_client.remove_environments(environment_ids)

    def remove_environment(self, environment_id: str):
        """Remove an environment by its ID

        Args:
            environment_id (str): The ID of the environment to remove
        Returns:
            Environment: The environment
        """
        return self.rocket_client.remove_environment(environment_id)

    def create_environment(self, environment_id: str) -> EnvironmentTo:
        """Force the creation of an environment project already available in the system.
        If the environment is already created, it will be deleted and recreated.

        Args:
            environment_id (str): The ID of the environment to create
        Returns:
            Environment: The environment
        """
        return self.rocket_client.create_environment(environment_id)

    def create_environments(self, environment_creation: List[EnvironmentCreationTo]) -> List[EnvironmentTo]:
        """Register new environments and create them on the system only if required

        Args:
            environment_creation (EnvironmentCreationTo): The environment to create
        Returns:
            Environment: The environment
        """
        return self.rocket_client.create_environments(environment_creation)
