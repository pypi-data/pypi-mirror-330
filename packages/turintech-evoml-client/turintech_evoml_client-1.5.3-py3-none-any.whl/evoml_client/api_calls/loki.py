# ───────────────────────────────── imports ────────────────────────────────── #
from enum import Enum
from typing import List, Dict, Any, Optional, Type, TypeVar

import requests
from pydantic import BaseModel, Field, ValidationError

from evoml_client.api_calls.utils import get_auth, check_status_code, get_url, is_url_https, REQUEST_TIMEOUT
from evoml_client.trial_conf_models import BudgetMode


# ──────────────────────────────────────────────────────────────────────────── #


def get_budget(allocation_mode: BudgetMode, models: List[dict]) -> Dict[str, float]:
    """Gets the calculated budget for a given trial config"""
    target_url = f"{get_url('loki')}/processes/info/evoml/budget"
    request_json = {
        "budgetAllocationMode": allocation_mode.name,
        "mlModels": models,
    }
    response = requests.post(
        url=target_url,
        json=request_json,
        headers=get_auth(),
        verify=is_url_https("loki"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return response.json()


class TaskStatus(str, Enum):
    CREATED = "created"
    PENDING = "pending"
    RUNNING = "running"
    REQUEUED = "requeued"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


class TaskInfo(BaseModel):
    id: str
    type: str


class ProcessInfo(BaseModel):
    id: str = Field(alias="_id")
    status: TaskStatus
    tasks: List[TaskInfo]


class PredictFileInfo(BaseModel):
    """Information about a file uploaded to loki"""

    id: str = Field(alias="_id")
    originalFilename: str


class PredictProcessInfo(BaseModel):
    """Information about a prediction process"""

    id: str = Field(alias="_id")
    processId: str
    taskId: str
    original: bool
    predictionFileId: Optional[str]
    predictionFile: Optional[PredictFileInfo]
    uploadedFileId: str
    uploadedFile: Optional[PredictFileInfo]
    createdAt: str


def start_single_async_task(task_type: str, task_params: Dict[str, Any]) -> ProcessInfo:
    """Creates and queues a task in loki returns task info"""
    target_url = f"{get_url('loki')}/processes/create/generic-single"
    request_json = {"task": {"type": task_type, "params": task_params, "depends": []}, "metadata": {}}
    response = requests.post(
        url=target_url,
        json=request_json,
        headers=get_auth(),
        verify=is_url_https("loki"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 202)
    return ProcessInfo.parse_obj(response.json())


ModelT = TypeVar("ModelT", bound=BaseModel)


def get_task_result(task_id: str, expected_response_model: Type[ModelT]) -> Optional[ModelT]:
    """
    Gets task result from loki and attempts to load it into the given expected_response_model.
    If the response doesn't match the expected_response_model, None is returned
    """
    target_url = f"{get_url('loki')}/results/{task_id}"
    response = requests.get(
        url=target_url,
        headers=get_auth(),
        verify=is_url_https("loki"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    try:
        result = expected_response_model.parse_obj(response.json())
    except ValidationError as err:
        result = None
    return result


def get_prediction_history(
    optimization_id: str, model_id: str, pipeline_zip_file_id: str, test_file_id: str
) -> PredictProcessInfo:
    """Gets the prediction history for a given trial config"""
    target_url = f"{get_url('loki')}/optimisations/{optimization_id}/models/{model_id}/prediction-history"
    request_json = {"pipelineZipFileId": pipeline_zip_file_id, "testFileId": test_file_id}
    response = requests.post(
        url=target_url,
        json=request_json,
        headers=get_auth(),
        verify=is_url_https("loki"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return PredictProcessInfo.parse_obj(response.json())
