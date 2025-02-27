# ───────────────────────────────── imports ────────────────────────────────── #
# Source imports
from time import sleep
from typing import Optional

from core_logging import logger
from rocket_rest.tos.pipeline_tos import PipelineReportTo
from core_rest_clients.api_client_exceptions import ClientException
from evoml_client.api_calls import trial_id_to_optimization_id
from evoml_client.models import Pipeline

# Service imports
from service.helpers.pipeline_mgr import PipelineHelper

# ────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                          specifies all modules that shall be loaded and the                            #
#                          imported into the current namespace when us use                               #
#                          from package import *                                                         #
# ─────────────────────────────────────────────────────────────────────────────────────────────────────  #

__all__ = ["PipelineGenerator"]

# ────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                        EvoML Pipeline Generator                                        #
# ────────────────────────────────────────────────────────────────────────────────────────────────────── #

# Disable core_rest_clients logger. The reason is that when we kick off the pipeline generation, we have a polling
# mechanism that will keep checking the status of the pipeline. This will cause the logger to be spammed with
# multiple error messages.
# Source: core_rest_clients/api_client_utils.py#L51
logger.disable("core_rest_clients")


class PipelineGenerator:
    """This is a pipeline generator implementation for EvoML"""

    pipeline_helper: Optional[PipelineHelper] = None

    def __init__(self):
        """Initialize the pipeline generator"""
        self.pipeline_helper = PipelineHelper()

    def generate_pipeline(self, pipeline: Pipeline) -> PipelineReportTo:
        """
        Generate a pipeline zip file for the specific pipeline in the trial.
        """
        if not pipeline.trialId:
            raise ValueError("Pipeline must have a trialId")
        optimization_id = trial_id_to_optimization_id(pipeline.trialId)
        if not optimization_id:
            raise ValueError(f"No optimization found for trial {pipeline.trialId}")
        created_pipeline = self.pipeline_helper.create_optimization_model_pipeline(optimization_id, pipeline.id)
        best_result = self.get_pipeline_report_when_ready(created_pipeline.pipeline_id, timeout=600)
        return best_result

    def get_pipeline_report_when_ready(self, pipeline_id: str, timeout: int = 600, interval: int = 5):
        result = None
        total = 0
        logger.info(f"Waiting for pipeline report with id {pipeline_id} to be ready.")
        while result is None:
            if total > timeout:
                logger.error(f"Pipeline report with id {pipeline_id} not ready after {timeout} seconds")
                raise ValueError(f"Pipeline report with id {pipeline_id} not ready after {timeout} seconds")
            try:
                result = self.pipeline_helper.get_pipeline_report_by_id(pipeline_id)
                logger.info("Pipeline report is now completed.")
            except ClientException:
                logger.info(f"Pipeline report with id {pipeline_id} not ready yet. Waiting for {interval} seconds.")
                sleep(interval)
                total += interval
                result = None
        return result

    def get_generated_pipeline(self, pipeline_id: str):
        """
        Get a generated pipeline by its ID.
        """
        existing_pipeline = self.pipeline_helper.get_pipeline_report_by_id(pipeline_id)
        if existing_pipeline is None:
            raise ValueError(f"No pipeline with id {pipeline_id} found.")
        return existing_pipeline
