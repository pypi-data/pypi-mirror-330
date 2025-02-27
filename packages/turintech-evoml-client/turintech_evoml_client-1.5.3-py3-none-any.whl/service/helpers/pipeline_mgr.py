# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Optional, List

# Core Source imports
from core_rest_clients.api_client_conf import ApiClientConf
from core_common_data_types.type_definitions import PositionType
from core_pagination.pagination_tos import PaginationTo, PaginationQueryParams

# Source imports
from rocket_client.pipeline_client import PipelineClient
from rocket_client.models import CreateOptimizationPipelineTo, OptimizationPipelineTo, PipelinesTo
from rocket_rest.tos.pipeline_tos import PipelineTo, PipelineReportTo, PipelineCreationTo, PipelineCreationOptionsTo
from rocket.data_types.pipeline_types import PipelineStatus
from rocket.dtos.pipeline_dtos import EvomlPipelineCreation
from evoml_client.api_calls import get_url, get_auth

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["PipelineHelper"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                   Pipeline Helper                                                    #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
class PipelineHelper:
    """This is a pipeline helper implementation for Rocket"""

    def __init__(self):
        self.rocket_client = PipelineClient(
            ApiClientConf(
                host=get_url("rocket"),
                port=None,
                postfix=None,
                headers=get_auth(),
            )
        )

    def get_all_pipelines(
        self,
        pipeline_ids: Optional[List[str]] = None,
        status: Optional[PipelineStatus] = None,
        page: int = 1,
        per_page: int = 10,
    ) -> PaginationTo[PipelineTo]:
        """Get all pipelines

        Args:
            pipeline_ids (Optional[List[str]], optional): The IDs of the pipelines to retrieve. Defaults to None.
            status (Optional[PipelineStatus], optional): The status of the pipelines to retrieve. Defaults to None.
            page (int, optional): The page number. Defaults to 1.
            per_page (int, optional): The number of items per page. Defaults to 10.
        Returns:
            Pagination: The list of pipelines
        """
        return self.rocket_client.get_pipelines(
            PipelinesTo(
                pipeline_ids=pipeline_ids, status=status, pagination=PaginationQueryParams(page=page, per_page=per_page)
            )
        )

    def get_pipeline_by_id(self, pipeline_id: str) -> PipelineTo:
        """Get a pipeline by its ID

        Args:
            pipeline_id (str): The ID of the pipeline to retrieve
        Returns:
            Pipeline: The pipeline
        """
        return self.rocket_client.get_pipeline(pipeline_id)

    def get_pipeline_report_by_id(self, pipeline_id: str) -> PipelineReportTo:
        """Get a pipeline report by its ID

        Args:
            pipeline_id (str): The ID of the pipeline to retrieve
        Returns:
            PipelineReport: The pipeline report
        """
        return self.rocket_client.get_pipeline_report(pipeline_id)

    def update_pipeline(self, pipeline_id: str, pipeline: PipelineTo) -> PipelineTo:
        """Update a pipeline by its ID

        Args:
            pipeline_id (str): The ID of the pipeline to update
            pipeline (Pipeline): The pipeline to update
        Returns:
            Pipeline: The pipeline
        """
        return self.rocket_client.update_pipeline(pipeline_id, pipeline)

    def remove_pipelines(self, pipeline_ids: Optional[List[str]]) -> PipelineTo:
        """Remove a list of pipelines by their IDs

        Args:
            pipeline_ids (Optional[List[str]]): The IDs of the pipelines to remove
        Returns:
            Pipeline: The pipeline
        """
        return self.rocket_client.remove_pipelines(pipeline_ids)

    def remove_pipeline(self, pipeline_id: str) -> PipelineTo:
        """Remove a pipeline by its ID

        Args:
            pipeline_id (str): The ID of the pipeline to remove
        Returns:
            Pipeline: The pipeline
        """
        return self.rocket_client.remove_pipeline(pipeline_id)

    def get_optimization_model_pipeline(
        self,
        optimization_id: str,
        model_id: str,
        status: Optional[PipelineStatus] = None,
        position: Optional[PositionType] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> PaginationTo[PipelineTo]:
        """Get a list of pipelines by their IDs and status

        Args:
            optimization_id (str): The ID of the optimization to retrieve
            model_id (str): The ID of the model to retrieve
            status (Optional[PipelineStatus], optional): The status of the pipelines to retrieve. Defaults to None.
            position (Optional[PositionType], optional): Whether to get the first or last Pipeline report.
                Defaults to None.
            page (int, optional): The page number. Defaults to 1.
            per_page (int, optional): The number of items per page. Defaults to 10.
        Returns:
            Pagination: The list of pipelines
        """
        return self.rocket_client.get_optimization_model_pipeline(
            optimization_id, model_id, status, position, page, per_page
        )

    def get_optimization_model_pipeline_report(
        self,
        optimization_id: str,
        model_id: str,
        status: Optional[PipelineStatus] = None,
        position: Optional[PositionType] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> PaginationTo[PipelineReportTo]:
        """Get a list of pipelines by their IDs and status

        Args:
            optimization_id (str): The ID of the optimization to retrieve
            model_id (str): The ID of the model to retrieve
            status (Optional[PipelineStatus], optional): The status of the pipelines to retrieve. Defaults to None.
            position (Optional[PositionType], optional): Whether to get the first or last Pipeline report.
                Defaults to None.
            page (int, optional): The page number. Defaults to 1.
            per_page (int, optional): The number of items per page. Defaults to 10.
        Returns:
            Pagination: The list of pipelines
        """
        return self.rocket_client.get_optimization_model_pipeline_report(
            OptimizationPipelineTo(
                optimization_id=optimization_id,
                model_id=model_id,
                status=status,
                position=position,
                pagination=PaginationQueryParams(page, per_page),
            )
        )

    def create_optimization_model_pipelines(
        self, evoml_pipelines: List[EvomlPipelineCreation]
    ) -> PaginationTo[PipelineCreationTo]:
        """Create a list of pipelines by their IDs and status

        Args:
            evoml_pipelines (List[EvomlPipelineCreation]): The list of pipelines to create
        Returns:
            Pagination: The list of pipelines
        """
        return self.rocket_client.create_optimization_model_pipelines(evoml_pipelines)

    def create_optimization_model_pipeline(
        self, optimization_id: str, model_id: str, options: PipelineCreationOptionsTo = PipelineCreationOptionsTo()
    ) -> PipelineCreationTo:
        """Create a list of pipelines by their IDs and status

        Args:
            optimization_id (str): The ID of the optimization to retrieve
            model_id (str): The ID of the model to retrieve
            options (PipelineCreationOptionsTo): The options to create the pipeline
        Returns:
            Pagination: The list of pipelines
        """
        return self.rocket_client.create_optimization_model_pipeline(
            CreateOptimizationPipelineTo(optimization_id=optimization_id, model_id=model_id, options=options)
        )
