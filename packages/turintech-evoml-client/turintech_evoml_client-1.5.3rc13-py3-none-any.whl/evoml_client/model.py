# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations
import json
from pathlib import Path
from zipfile import ZipFile
from typing import Union, List, Dict, Optional
from enum import Enum

import numpy as np
import pandas as pd

from pydantic import BaseModel, validator

from evoml_client.api_calls import (
    download_path,
    download_pipeline,
    trial_id_to_optimization_id,
    get_task_result,
    download_predictions,
    get_file_id,
    poll_status_task,
    get_prediction_history,
)
from evoml_client.utils import import_pipeline_conf_mgr, import_pipeline_module, sanitise_headers
from evoml_client.dataset import Dataset, DatasetState
from service.helpers.pipeline_mgr import PipelineHelper


# ──────────────────────────────────────────────────────────────────────────── #


# ──────────────────────────────── Exceptions ──────────────────────────────── #


class IncompatibleModel(Exception):
    def __init__(self):
        super().__init__("The other model is not comparable")


# ──────────────────────────────────────────────────────────────────────────── #


class ModelVersion(str, Enum):
    cloud_trained = "cloud"
    local_trained = "local"


class ModelRepresentation(BaseModel):
    name: str
    mlModelName: str
    scores: dict
    pipelineId: str
    metrics: dict
    pipelineZipFileId: str
    predictionCsvFileId: str


class OnlinePredictionResult(BaseModel):
    resultType: str
    content: Dict[str, str]

    @validator("resultType")
    def result_type_must_be_predict(cls, v):
        if v != "predict":
            raise ValueError("expected resultType = predict")
        return v


class Model:
    """
    ACTIONS:
        init(trial_result, pipeline) -- return model from a trial result and pipeline
        build_model() -- return the underlying python object live loaded from zip
        get_pipline() -- return path of the downloaded pipeline.zip
        fit() -- Requires build_model to have been run
        predict() -- Requires build_model to have been run
        predict_online() -- Run the model using evoml's instant predictions feature

    COMPARISONS: __eq__(), __ne__(), __lt__(), __le__(), __gt__(), __ge__()
        given a Model with the same set of score metrics, perform
        relevant comparison -- NOT SURE HOW USEFUL THIS IS --
    """

    # ──────────────────────────── Constructors ────────────────────────────── #
    def __init__(self, trial_id: str, **params):
        self.__pipeline_unpacked = None
        self.__pipeline_zip = None
        self._pipeline_handler = None
        self.target_index = 0
        self.model_rep = ModelRepresentation(**params)
        self.trial_id = trial_id
        self._pipeline_helper = PipelineHelper()

    @classmethod
    def _from_result(cls, result: dict, pipeline_data: dict, trial_id: str) -> Model:
        """Internal method"""
        metrics = {}
        for name, runs in pipeline_data["metrics"].items():
            metric = {}
            for situation, stats in runs.items():
                if stats is not None:
                    metric[situation] = {
                        "min": stats["min"],
                        "max": stats["max"],
                        "average": stats["average"],
                        "median": stats["median"],
                    }
                else:
                    metric[situation] = None
            metrics[name] = metric
        model = cls(
            name=pipeline_data["name"],
            mlModelName=pipeline_data["mlModelName"],
            scores=pipeline_data["scores"],
            pipelineId=result.get("pipelineId", ""),
            metrics=metrics,
            pipelineZipFileId=result.get("pipelineZipFileId", ""),
            predictionCsvFileId=result.get("predictionCsvFileId", ""),
            trial_id=trial_id,
        )
        return model

    # ──────────────────────── Platform Interactions ───────────────────────── #
    def predict_online(self, dataset: Dataset, timeout: int = 2**63) -> Optional[pd.DataFrame]:
        """
        Run the model using evoml's instant predictions feature on the given
        dataset. Uploads the dataset if the dataset is offline, block until
        prediction results are available. This method will block until the
        prediction is complete or the timeout value (in seconds) is reached.
        """
        # Validate dataset
        if dataset.get_state() == DatasetState.OFFLINE:
            dataset.put()
        assert dataset.get_state() == DatasetState.ONLINE

        self._populate_pipeline_zip_id()
        optimization_id = trial_id_to_optimization_id(self.trial_id)
        if optimization_id is None:
            raise ValueError("Trial is not part of an optimization")

        process_info = get_prediction_history(
            optimization_id=optimization_id,
            model_id=self.model_rep.pipelineId,
            pipeline_zip_file_id=self.model_rep.pipelineZipFileId,
            test_file_id=get_file_id(dataset.dataset_id),
        )

        # Block for Task Completion or Timeout, Return None if the terminal state reached isn't success
        # Cannot use poll_status at least for now, because enigma does not store predict process in the current release.
        if not poll_status_task(process_info.taskId, timeout, 2):
            return None

        # Return Predict output
        pred_task_result: OnlinePredictionResult = get_task_result(process_info.taskId, OnlinePredictionResult)
        pred_file_id: Optional[str] = pred_task_result.content.get("predictionFileId", None)
        if pred_file_id is None:
            return None
        prediction_file_path = download_predictions(
            self.trial_id, self.model_rep.pipelineId, process_info.taskId, pred_file_id
        )
        prediction_dataframe = pd.read_parquet(prediction_file_path)
        return prediction_dataframe

    # ───────────────────────────── Live loading ───────────────────────────── #
    def build_model(self) -> None:
        """REQUIRES evoml-client[full]\n Load the ML model into python"""
        try:
            from evoml_pipeline_interface import PipelineProjectExtendedConf
        except ModuleNotFoundError as err:
            print(f"pip install evoml_client[full] to use this method")
            return
        self.__pipeline_zip = self.get_pipeline()
        self.__pipeline_unpacked = self.get_pipeline().with_suffix("")
        if not self.__pipeline_unpacked.exists():
            with ZipFile(self.__pipeline_zip, "r") as zip_obj:
                zip_obj.extractall(self.__pipeline_unpacked)

        self.conf_mgr = import_pipeline_conf_mgr(self.__pipeline_unpacked)

        import_pipeline_module(pipeline_root=self.__pipeline_unpacked)
        from pipeline.pipeline_handler import PipelineHandler

        self._pipeline_handler = PipelineHandler(self.conf_mgr.pipeline_data_conf)

    def get_pipeline(self) -> Path:
        """Returns the local path of the files relating to this model"""
        target = Path(
            download_path(),
            "models",
            f"{self.model_rep.name}_{self.model_rep.pipelineId}.zip".replace("-", "_"),
        )
        self._populate_pipeline_zip_id()
        if not target.exists():
            download_pipeline(
                pipeline_zip_id=self.model_rep.pipelineZipFileId,
                model_name=self.model_rep.name,
                pipeline_id=self.model_rep.pipelineId,
            )
        return target

    def fit(
        self,
        data: Union[str, Path] = None,
        train_file: Path = None,
        test_file: Path = None,
    ):
        """
        REQUIRES evoml-client[full]\n
        Locally train the ML model against csv files. Either provide
        separate train and test files or allow the client to perform
        the splitting itself
        """
        self._pipeline_handler.train(train_file=train_file, test_file=test_file, data=data)

    def predict(
        self,
        data: Union[str, Path, pd.DataFrame, np.ndarray] = None,
    ) -> List:
        """
        REQUIRES evoml-client[full]\n
        Execute the ML model against the given pandas dataframe or csv file.
        Optionally specify the use of either the pre-trained model or a locally
        trained version. Only use the local version if the fit method has been
        previously called.
        """
        if self._pipeline_handler.model is None:
            print(f"pip install evoml_client[full] to use this method")
            return None

        loaded_data: pd.DataFrame = self.read_predict_data(data)

        raw_predictions = self._pipeline_handler.run_prediction(loaded_data)
        if len(loaded_data.index) == 1:
            predictions = raw_predictions[self._pipeline_handler.field_predictions][0]
        else:
            predictions = raw_predictions[self._pipeline_handler.field_predictions]
        return predictions

    def predict_proba(
        self,
        data: Union[str, Path, pd.DataFrame, np.ndarray] = None,
        model_version: ModelVersion = ModelVersion.cloud_trained,
    ) -> List:
        """
        REQUIRES evoml-client[full]\n
        Execute the ML model against the given pandas dataframe or csv file.
        Optionally specify the use of either the pre-trained model or a locally
        trained version. Only use the local version if the fit method has been
        previously called.
        """
        if self._pipeline_handler.model is None:
            print(f"pip install evoml_client[full] to use this method")
            return None

        loaded_data: pd.DataFrame = self.read_predict_data(data)

        if model_version == ModelVersion.local_trained:
            raise NotImplementedError("Local Predict proba is not yet implemented")
        else:
            raw_predictions = self._pipeline_handler.run_prediction(loaded_data)
            if len(loaded_data.index) == 1:
                predictions = raw_predictions[self._pipeline_handler.field_probabilities][0]
            else:
                predictions = raw_predictions[self._pipeline_handler.field_probabilities]
        return predictions

    def _populate_pipeline_zip_id(self):
        pipeline_results = self._pipeline_helper.get_pipeline_report_by_id(self.model_rep.pipelineId)
        self.model_rep.pipelineZipFileId = pipeline_results.pipeline_zip_file_id

    def read_predict_data(self, data: Union[str, Path, pd.DataFrame, np.ndarray]) -> pd.DataFrame:
        with open(self.conf_mgr.pipeline_data_conf.predict_config_file_path) as json_file:
            config: Dict = json.load(json_file)

        is_time_series = config.get("is_time_series")
        index_column = config.get("date_column") if is_time_series else False

        if isinstance(data, (str, Path)):
            loaded_data = pd.read_csv(data, index_col=index_column)
        elif isinstance(data, np.ndarray):
            data_width = 1 if data.ndim == 1 else data.shape[1]
            loaded_data = pd.DataFrame(data=data, columns=[f"col{i}" for i in range(data_width)])
        else:
            loaded_data = data

        original_headers = list(loaded_data.columns)
        clean_headers = sanitise_headers(original_headers)

        if clean_headers != original_headers:
            loaded_data = loaded_data.rename(
                columns={name: clean for name, clean in zip(original_headers, clean_headers)},
            )

        return loaded_data

    # ────────────────────────────── Comparison ────────────────────────────── #

    def __validate_comparison__(self, other: Model):
        if self.model_rep.scores.keys() != other.model_rep.scores.keys():
            raise IncompatibleModel

    def __eq__(self, other: Model) -> bool:
        self.__validate_comparison__(other)
        result = True
        for metric in self.model_rep.scores.keys():
            result = self.model_rep.scores[metric] == other.model_rep.scores[metric]
            if not result:
                break
        return result

    def __ne__(self, other: Model) -> bool:
        self.__validate_comparison__(other)
        result = True
        for metric in self.model_rep.scores.keys():
            result = self.model_rep.scores[metric] != other.model_rep.scores[metric]
            if not result:
                break
        return result

    def __lt__(self, other: Model) -> bool:
        self.__validate_comparison__(other)
        result = True
        for metric in self.model_rep.scores.keys():
            result = self.model_rep.scores[metric] < other.model_rep.scores[metric]
            if not result:
                break
        return result

    def __le__(self, other: Model) -> bool:
        self.__validate_comparison__(other)
        result = True
        for metric in self.model_rep.scores.keys():
            result = self.model_rep.scores[metric] <= other.model_rep.scores[metric]
            if not result:
                break
        return result

    def __gt__(self, other: Model) -> bool:
        self.__validate_comparison__(other)
        result = True
        for metric in self.model_rep.scores.keys():
            result = self.model_rep.scores[metric] > other.model_rep.scores[metric]
            if not result:
                break
        return result

    def __ge__(self, other: Model) -> bool:
        self.__validate_comparison__(other)
        result = True
        for metric in self.model_rep.scores.keys():
            result = self.model_rep.scores[metric] >= other.model_rep.scores[metric]
            if not result:
                break
        return result

    # ───────────────────────────── Dirty Type Helper ──────────────────────────── #
    def __rebuild_type(self, value: str) -> Union[bool, int, str, float, None]:
        if value == "True":
            return True
        if value == "False":
            return False
        if value == "None":
            return None

        try:
            return int(value)
        except (ValueError, TypeError):
            pass

        try:
            return float(value)
        except (ValueError, TypeError):
            pass

        return value
