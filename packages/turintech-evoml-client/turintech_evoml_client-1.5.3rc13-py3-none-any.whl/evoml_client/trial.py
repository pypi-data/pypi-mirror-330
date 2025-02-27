# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

import uuid
from typing import List, Tuple, Union, Optional
from enum import Enum

import pandas as pd
import numpy as np

from evoml_client.models import Pipeline, Status
from evoml_client.pipeline import PipelineGenerator
from evoml_client.trial_conf_models import MlTask, BudgetMode
from evoml_client.dataset import Dataset, DatasetState
from evoml_client.trial_config import TrialConfig
from evoml_client.model import Model
from evoml_client.api_calls import (
    trial_post,
    trial_get,
    trial_start,
    get_url,
    poll_status,
    get_process_info,
    StatusCodeException,
    get_data_info,
    get_permitted_models,
    get_loss_funcs,
    find_loss_func,
    get_trial_pipelines,
    get_trial_pipeline_by_id,
    trial_id_to_optimization_id,
    dataset_get,
)

# ──────────────────────────────────────────────────────────────────────────── #


class TrialState(Enum):
    OFFLINE = 0
    ONLINE = 1
    RUNNING = 2
    FINISHED = 3
    FAILED = 4


class MetricScope(str, Enum):
    validation = "validation"
    train = "train"
    test = "test"


# ──────────────────────────────── Exceptions ──────────────────────────────── #
class IncompatibleTrialState(Exception):
    def __init__(self, state: TrialState, required: List[TrialState], operation: str):
        super().__init__(
            f"Trial is in incorrect state for this operation - "
            f"Trial is {state}, must be in {required} to {operation}"
        )


class Trial:
    """
    States:
        OFFLINE -- url and id are not initialised, interactive config step\n
        ONLINE -- url and id are assigned, config and dataset are on platform\n
        RUNNING -- ONLINE and optimization underway\n
        FINISHED -- ONLINE and optimization complete\n
    Actions:
        run prefixed inits are used to define and wait for the trial in 1 line\n
        init(Dataset(ONLINE), TrialConfig) -- Create Trial in OFFLINE\n
        init(Dataset(OFFLINE), TrialConfig) -- Create Trial in OFFLINE, transition DS to ONLINE\n
        init(Raw, TrialConfig) -- Create Trial in OFFLINE, Create DS in OFFLINE, transition DS to ONLINE\n
        init(URL) -- Create Trial in ONLINE/RUNNING/FINISHED, Create DS in ONLINE\n
        init(ID) -- Create Trial in ONLINE/RUNNING/FINISHED, Create DS in ONLINE\n
        init(DS_URL) -- Create Trial in OFFLINE, Create DS in ONLINE\n
        init(DS_ID) -- Create Trial in OFFLINE, Create DS in ONLINE\n
        put() -- Transition from OFFLINE to ONLINE\n
        start() -- Transition from ONLINE to RUNNING\n
        wait() -- block until transition from RUNNING to FINISHED\n
        run() -- block and Transition from OFFLINE to FINISHED\n
        get_progress() -- Update progress, Stay RUNNING or transition to FINISHED.\n
        get_best() -- stay FINISHED\n
        get_models() -- stay FINISHED\n
        get_state() -- if URL exists & prog = -1.0 -> ONLINE,\n
                    -- if URL exists & has optimization -> RUNNING,\n
                    -- if URL exists & has optimization & prog = 1 -> FINISHED\n
    """

    # ──────────────────────────── Constructors ────────────────────────────── #
    def __init__(self):
        self.url: str = None
        self.trial_id: str = None
        self.optimization_id: str = None
        self.name: str = None
        self.dataset: Dataset = None
        self.target_col = 0
        self.config: TrialConfig = None
        self.progress: float = -1.0
        self.tags: List[str] = None
        self.pipeline_generator = PipelineGenerator()

    @classmethod
    def from_dataset(
        cls,
        dataset: Dataset,
        trial_name: str,
        target_col: Union[int, str],
        config: Optional[TrialConfig] = None,
        tags: List[str] = None,
    ) -> Tuple[Trial, Dataset]:
        """
        Build a trial object given a dataset object, if the dataset is OFFLINE
        this method uploads and waits for the dataset to be ready before
        returning.
        """
        trial = cls()
        trial.name = trial_name
        trial.tags = tags
        if dataset.get_state() == DatasetState.OFFLINE:
            dataset.put()
        if isinstance(target_col, int):
            trial.target_col = target_col
        else:
            trial.target_col = dataset._find_column_by_name(target_col)
        dataset.wait()
        trial.dataset = dataset
        if config is not None:
            trial.config = config
            return trial, dataset
        trial.config = trial._infer_config(dataset=dataset, target_col_index=trial.target_col)
        return trial, trial.dataset

    @classmethod
    def from_data_file(
        cls,
        fname: str,
        trial_name: str,
        target_col: Union[int, str],
        config: Optional[TrialConfig] = None,
        tags: List[str] = None,
    ) -> Tuple[Trial, Dataset]:
        """
        Blocking. Build a trial object given a data file, uploads and waits
        for the dataset to be ready before returning. Returns a trial and dataset
        as a tuple
        """
        trial = cls()
        trial.name = trial_name
        trial.tags = tags
        dataset = Dataset.from_file(fname=fname, name=fname.split("/")[-1].split(".")[0])
        if isinstance(target_col, int):
            trial.target_col = target_col
        else:
            trial.target_col = dataset._find_column_by_name(target_col)
        dataset.put()
        dataset.wait()
        trial.dataset = dataset
        if config is not None:
            trial.config = config
            return trial, dataset
        trial.config = trial._infer_config(dataset=dataset, target_col_index=trial.target_col)
        return trial, trial.dataset

    @classmethod
    def from_pandas(
        cls,
        data: pd.DataFrame,
        data_name: str,
        target_col: Union[int, str],
        trial_name: str,
        config: Optional[TrialConfig] = None,
        tags: List[str] = None,
    ) -> Tuple[Trial, Dataset]:
        """
        Blocking. Build a trial object given a data file, uploads and waits
        for the dataset to be ready before returning. Returns a trial and dataset
        as a tuple
        """
        trial = cls()
        trial.name = trial_name
        trial.tags = tags
        dataset = Dataset.from_pandas(data, data_name)
        if isinstance(target_col, int):
            trial.target_col = target_col
        else:
            trial.target_col = dataset._find_column_by_name(target_col)
        dataset.put()
        dataset.wait()
        trial.dataset = dataset
        if config is not None:
            trial.config = config
            return trial, dataset
        trial.config = trial._infer_config(dataset=dataset, target_col_index=trial.target_col)
        return trial, trial.dataset

    @classmethod
    def from_numpy(
        cls,
        data: np.ndarray,
        data_name: str,
        target_col: int,
        trial_name: str,
        config: Optional[TrialConfig] = None,
        tags: List[str] = None,
    ) -> Tuple[Trial, Dataset]:
        """
        Blocking. Build a trial object given a numpy array, uploads and waits
        for the dataset to be ready before returning. Returns a trial and dataset
        as a tuple
        """
        trial = cls()
        trial.name = trial_name
        trial.tags = tags
        dataset = Dataset.from_numpy(data, data_name)
        dataset.put()
        dataset.wait()
        trial.dataset = dataset
        trial.target_col = target_col
        if config is not None:
            trial.config = config
            return trial, dataset
        trial.config = trial._infer_config(dataset=dataset, target_col_index=trial.target_col)
        return trial, trial.dataset

    @classmethod
    def from_numpy_xy(
        cls,
        data_x: np.ndarray,
        data_y: np.ndarray,
        data_name: str,
        trial_name: str,
        config: Optional[TrialConfig] = None,
        tags: List[str] = None,
    ) -> Tuple[Trial, Dataset]:
        """"""
        trial = cls()
        trial.name = trial_name
        trial.tags = tags
        dataset = Dataset.from_numpy_xy(data_x=data_x, data_y=data_y, name=data_name)
        dataset.put()
        dataset.wait()
        trial.dataset = dataset
        trial.target_col = dataset._find_column_by_name("col{}".format(len(dataset.data.columns) - 1))
        if config is not None:
            trial.config = config
            return trial, dataset
        trial.config = trial._infer_config(dataset=dataset, target_col_index=trial.target_col)
        return trial, trial.dataset

    @classmethod
    def from_dataset_url(
        cls,
        ds_url: str,
        target_col: Union[int, str],
        trial_name: str,
        config: Optional[TrialConfig] = None,
        tags: List[str] = None,
    ) -> Tuple[Trial, Dataset]:
        """
        Build a trial object given a URL of a dataset on the same env as
        specified in the most recent client initialisation. Returns a trial
        and dataset as a tuple
        """
        trial = cls()
        trial.name = trial_name
        trial.tags = tags
        dataset = Dataset.from_url(ds_url)
        if isinstance(target_col, int):
            trial.target_col = target_col
        else:
            trial.target_col = dataset._find_column_by_name(target_col)
        trial.dataset = dataset
        if config is not None:
            trial.config = config
            return trial, dataset
        trial.config = trial._infer_config(dataset=dataset, target_col_index=trial.target_col)
        return trial, dataset

    @classmethod
    def from_dataset_id(
        cls,
        dataset_id: str,
        target_col: Union[int, str],
        trial_name: str,
        config: Optional[TrialConfig] = None,
        tags: List[str] = None,
    ) -> Tuple[Trial, Dataset]:
        """
        Build a trial object given an ID of a dataset on the same env as
        specified in the most recent client initialisation. Returns a trial
        and dataset as a tuple
        """
        trial = cls()
        trial.name = trial_name
        trial.tags = tags
        dataset = Dataset.from_id(dataset_id)
        if isinstance(target_col, int):
            trial.target_col = target_col
        else:
            trial.target_col = dataset._find_column_by_name(target_col)
        trial.dataset = dataset
        if config is not None:
            trial.config = config
            return trial, dataset
        trial.config = trial._infer_config(dataset=dataset, target_col_index=trial.target_col)
        return trial, trial.dataset

    @classmethod
    def from_url(cls, url: str) -> Tuple[Trial, Dataset]:
        """
        Get a local representation of a trial on the platform given a URL
        on the same env as specified in the most recent client initialisation.
        Returns a trial and dataset as a tuple.
        URL should end /trials/optimize/id
        """
        trial = cls()
        if url.split("/")[-3:-1] == ["trials", "optimize"]:
            trial.url = url  # URL expected to be /trials/optimize/id
        else:
            raise ValueError(f"{url} is invalid - must be <Platform>/trials/optimize/<ID>")
        trial.trial_id = trial.url.split("/")[-1]
        result = trial_get(trial.trial_id)
        trial.optimization_id = result["optimizationProcessId"] if "optimizationProcessId" in result else None
        trial.name = result["name"]
        trial.dataset = Dataset.from_id(result["datasetId"])
        trial.target_col = result["columnIndex"]
        trial.config = TrialConfig().with_params(result["options"])
        if trial.optimization_id is not None:
            trial.get_progress()
        return trial, trial.dataset

    @classmethod
    def from_id(cls, trial_id: str) -> Tuple[Trial, Dataset]:
        """
        Get a local representation of a trial on the platform given an ID
        on the same env as specified in the most recent client initialisation.
        Returns a trial and dataset as a tuple.
        """
        trial = cls()
        trial.trial_id = trial_id
        trial.url = f"{get_url('platform')}/trials/optimize/{trial_id}"
        try:
            result = trial_get(trial.trial_id)
        except StatusCodeException as err:
            raise ValueError(f"{id} is not a valid dataset ID or connection failed: {str(err)}")
        trial.optimization_id = result["optimizationProcessId"] if "optimizationProcessId" in result else None
        trial.name = result["name"]
        trial.dataset = Dataset.from_id(result["datasetId"])
        trial.target_col = result["columnIndex"]
        trial.config = TrialConfig().with_params(result["options"])
        if trial.optimization_id is not None:
            trial.get_progress()
        return trial, trial.dataset

    @classmethod
    def run_from_dataset(
        cls,
        dataset: Dataset,
        trial_name: str,
        target_col: Union[int, str],
        config: Optional[TrialConfig] = None,
        timeout: int = -1,
    ) -> Tuple[Trial, Dataset]:
        """
        Blocking. Same as from_dataset, but also runs & waits for the trial
        """
        trial, dataset = cls.from_dataset(
            dataset=dataset,
            trial_name=trial_name,
            target_col=target_col,
            config=config,
        )
        trial.run(timeout=timeout)
        return trial, dataset

    @classmethod
    def run_from_data_file(
        cls,
        fname: str,
        trial_name: str,
        target_col: Union[int, str],
        config: Optional[TrialConfig] = None,
        timeout: int = -1,
    ) -> Tuple[Trial, Dataset]:
        """
        Blocking. Same as from_data_file, but also runs & waits for the trial
        """
        trial, dataset = cls.from_data_file(
            fname=fname,
            trial_name=trial_name,
            target_col=target_col,
            config=config,
        )
        trial.run(timeout=timeout)
        return trial, dataset

    @classmethod
    def run_from_pandas(
        cls,
        data: pd.DataFrame,
        data_name: str,
        target_col: Union[int, str],
        trial_name: str,
        config: Optional[TrialConfig] = None,
        timeout: int = -1,
    ) -> Tuple[Trial, Dataset]:
        """
        Blocking. Same as from_pandas, but also runs & waits for the trial
        """
        trial, dataset = cls.from_pandas(
            data=data,
            data_name=data_name,
            target_col=target_col,
            trial_name=trial_name,
            config=config,
        )
        trial.run(timeout=timeout)
        return trial, dataset

    @classmethod
    def run_from_numpy(
        cls,
        data: np.ndarray,
        data_name: str,
        target_col: int,
        trial_name: str,
        config: Optional[TrialConfig] = None,
        timeout: int = -1,
    ) -> Tuple[Trial, Dataset]:
        """
        Blocking. Same as from_numpy, but also runs & waits for the trial
        """
        trial, dataset = cls.from_numpy(
            data=data,
            data_name=data_name,
            target_col=target_col,
            trial_name=trial_name,
            config=config,
        )
        trial.run(timeout=timeout)
        return trial, dataset

    @classmethod
    def run_from_dataset_url(
        cls,
        ds_url: str,
        target_col: Union[int, str],
        trial_name: str,
        config: Optional[TrialConfig] = None,
        timeout: int = -1,
    ) -> Tuple[Trial, Dataset]:
        """
        Blocking. Same as from_dataset_url, but also runs & waits for the trial
        """
        trial, dataset = cls.from_dataset_url(
            ds_url=ds_url,
            target_col=target_col,
            trial_name=trial_name,
            config=config,
        )
        trial.run(timeout=timeout)
        return trial, dataset

    @classmethod
    def run_from_dataset_id(
        cls,
        dataset_id: str,
        target_col: Union[int, str],
        trial_name: str,
        config: Optional[TrialConfig] = None,
        timeout: int = 0,
    ) -> Tuple[Trial, Dataset]:
        """
        Blocking. Same as from_dataset_id, but also runs & waits for the trial
        """
        trial, dataset = cls.from_dataset_id(
            dataset_id=dataset_id,
            target_col=target_col,
            trial_name=trial_name,
            config=config,
        )
        trial.run(timeout=timeout)
        return trial, dataset

    # ──────────────────────── Platform Interactions ───────────────────────── #
    def put(self, param_tune: bool = True) -> bool:
        """Upload the trial to the platform"""
        valid_states = [TrialState.OFFLINE]
        if self.get_state() not in valid_states:
            raise IncompatibleTrialState(self.get_state(), valid_states, "put")
        if not param_tune:
            for model in self.config.options.models:
                for param in model["parameters"]["inputParameters"]:
                    param["enabled"] = False
        result = trial_post(
            self.name,
            self.dataset.dataset_id,
            self.target_col,
            self.config.dict(),
            self.tags or ["evoml-client"],
        )
        self.trial_id = result["_id"]
        self.url = f"{get_url('platform')}/trials/optimize/{self.trial_id}"
        self.optimization_id = result["optimizationProcessId"]
        return True  # If the API was happy

    def start(self) -> float:
        """Trigger the start of the optimization trial"""
        valid_states = [TrialState.ONLINE]
        if self.get_state() not in valid_states:
            raise IncompatibleTrialState(self.get_state(), valid_states, "start")
        # Wait here for dataset to have a finished analysis
        result = trial_start(self.trial_id)
        self.optimization_id = result["optimizationProcessId"]
        self.progress = 0.0
        return self.get_progress()

    def wait(self, timeout: int = -1) -> bool:
        """
        Blocking. Wait for either the completion of the trial or for
        the specified timeout duration, whichever is shortest.
        Returns True if complete, False if a timeout occurred
        """
        valid_states = [TrialState.RUNNING, TrialState.FINISHED]
        if self.get_state() not in valid_states:
            raise IncompatibleTrialState(self.get_state(), valid_states, "wait")
        if timeout == -1:
            return poll_status(self.optimization_id, 2**63, 2)
        return poll_status(self.optimization_id, timeout, 2)

    def run(self, timeout: int = -1) -> bool:
        """
        Blocking. Starts and waits for the trial or for the timeout
        duration. Works with OFFLINE or ONLINE trials
        """
        valid_states = [TrialState.OFFLINE, TrialState.ONLINE]
        if self.get_state() not in valid_states:
            raise IncompatibleTrialState(self.get_state(), valid_states, "run")
        if not self.dataset_analysis_process_successful(self.dataset.dataset_id):
            raise Exception(f"Trial run failed as dataset analysis status not completed or failed.")
        if self.get_state() == TrialState.OFFLINE:
            self.put()
        self.start()
        return self.wait(timeout=timeout)

    def get_progress(self) -> float:
        """
        Get the current progress of the running trial. Returns
        between 0,1
        """
        valid_states = [TrialState.RUNNING, TrialState.FINISHED]
        if self.get_state() not in valid_states:
            raise IncompatibleTrialState(self.get_state(), valid_states, "get_progress")
        self.progress = get_process_info(self.optimization_id).progress
        return self.progress

    def dataset_analysis_process_successful(self, dataset_id: str) -> bool:
        dataset_info = dataset_get(dataset_id)
        analysis_process_id = dataset_info.get("response_json", {}).get("analysisProcessId")
        analysis_process_status = (
            get_process_info(analysis_process_id).status if analysis_process_id is not None else None
        )
        return analysis_process_status == Status.SUCCESS

    def sort_by_metric(self, d, loss_funcs, MetricScope) -> List:
        metrics = []
        for loss_func in loss_funcs:
            sign = -1 if loss_func["order"] == "asc" else 1
            data_part = getattr(d.metrics[loss_func["slug"]], MetricScope.value)
            if data_part:
                metrics.append(sign * data_part.average)
        return metrics

    def get_best_pipeline(self, results: List[Pipeline], metrics: List[str] = None, metricScope: MetricScope = None):
        """
        Method to get the best of the models in the trial.
        If the user wants the best model according to required metric(s),we can accept them as part of the input. Then,
        we find the correct scores and sort accordingly.
        If the user does not specify any metric, we will use the loss functions instead.
        """
        if len(results) == 1:
            result = results[0]
        else:
            if metrics:
                loss_ids = [find_loss_func(m, self.config.options.mlTask) for m in metrics]
            else:
                loss_ids = self.config.options.lossFunctionsIds
            all_loss_funcs = get_loss_funcs(self.config.options.mlTask)
            loss_funcs = [x for x in all_loss_funcs if x["_id"] in loss_ids]
            result = sorted(
                results,
                key=lambda d: self.sort_by_metric(d, loss_funcs, metricScope or MetricScope.validation),
                reverse=True,
            )[0]
        return result

    # ──────────────────────── Model Extraction with pipeline Generation ────────────────────────────── #
    def get_best(
        self, metrics: List[str] = None, metricScope: MetricScope = None, existing_pipeline_id: str = None
    ) -> Model:
        """
        Identifies the best model in the trial and returns pipeline with id existing_pipeline_id.
        If not specified, it will generate a new one.
        """
        valid_states = [TrialState.RUNNING, TrialState.FINISHED]
        if self.get_state() not in valid_states:
            raise IncompatibleTrialState(self.get_state(), valid_states, "get_best")
        pipelines = get_trial_pipelines(self.trial_id)
        if len(pipelines) == 0:
            raise Exception("No optimization results found")

        best_pipeline = self.get_best_pipeline(pipelines, metrics, metricScope)
        if existing_pipeline_id is None:
            best_result = self.pipeline_generator.generate_pipeline(best_pipeline)
        else:
            # In this case, we still identify the best result, but we do not generate a new pipeline.
            # Pipeline with id existing_pipeline_id is used.
            best_result = self.pipeline_generator.get_generated_pipeline(existing_pipeline_id)

        model = Model._from_result(
            result=best_result.dict(),
            pipeline_data=best_pipeline.dict(),
            trial_id=self.trial_id,
        )
        return model

    def get_optimization_model_pipeline_by_id(self, model_id: str, existing_pipeline_id: str = None) -> Model:
        """
        Identifies ml model with id model_id and returns pipeline with id existing_pipeline_id.
        If not specified, it will generate a new one.
        """
        pipelines = get_trial_pipelines(self.trial_id)
        if len(pipelines) == 0:
            raise Exception("No optimization results found")
        pipeline = next((p for p in pipelines if p.id == model_id), None)
        if pipeline is None:
            raise Exception(f"No model with id {model_id} found.")

        if existing_pipeline_id is None:
            result = self.pipeline_generator.generate_pipeline(pipeline)
        else:
            result = self.pipeline_generator.get_generated_pipeline(existing_pipeline_id)

        model = Model._from_result(
            result=result.dict(),
            pipeline_data=pipeline.dict(),
            trial_id=self.trial_id,
        )
        return model

    # ──────────────────────── Model Extraction without pipeline Generation ────────────────────────────── #

    def get_models(self) -> List[Model]:
        """
        Returns all models that have been evaluated over the trial,
        does not fully build any of them. But they still can be used for
        comparison etc.
        """
        valid_states = [TrialState.RUNNING, TrialState.FINISHED]
        if self.get_state() not in valid_states:
            raise IncompatibleTrialState(self.get_state(), valid_states, "get_models")
        pipelines = get_trial_pipelines(self.trial_id)

        models = []
        for pipeline in pipelines:
            models.append(Model._from_result(result={}, pipeline_data=pipeline.dict(), trial_id=self.trial_id))
        return models

    def get_model(self, optimization_id: str, model_id: str) -> Model:
        pipeline = get_trial_pipeline_by_id(optimization_id, model_id)
        return Model._from_result(result={}, pipeline_data=pipeline.dict(), trial_id=self.trial_id)

    def get_model_by_id(self, pipeline_id: str) -> Model:
        # 1-Map trialId from Thanos to optimizationId on BW
        optimization_id: str = trial_id_to_optimization_id(self.trial_id)
        # 2-Get all pipelines from black-widow and take the one that matches ID.
        return self.get_model(optimization_id, pipeline_id)

    # ──────────────────────── State Management ────────────────────────────── #
    def get_state(self) -> TrialState:
        """
        Returns current state of the trial: Offline, Online, Running, Finished
        """
        if self.url is None:
            return TrialState.OFFLINE

        if self.optimization_id is not None:
            status = get_process_info(self.optimization_id).status
            if status == Status.RUNNING:
                return TrialState.RUNNING
            elif status == Status.FAILED:
                return TrialState.FAILED
            elif status == Status.SUCCESS:
                return TrialState.FINISHED
            else:
                print("Couldnt match any status: ,status is" + status)
                return TrialState.RUNNING

        return TrialState.ONLINE

    # ──────────────────────────── General Helpers ─────────────────────────── #
    @staticmethod
    def _infer_config(dataset: Dataset, target_col_index: int) -> TrialConfig:
        all_columns = get_data_info(dataset.dataset_id)
        target_column_info = all_columns[target_col_index]["defaultTrialOptions"]
        ml_task: MlTask = MlTask.classification
        if not target_column_info["isValidTarget"]:
            raise ValueError(f"{target_col_index} is not a valid target")
        if target_column_info["mlTask"] == "forecasting":
            ml_task = MlTask.forecasting
        elif target_column_info["mlTask"] == "regression":
            ml_task = MlTask.regression
        loss_funcs = target_column_info["lossFunctionSlugs"]

        models = [
            model["name"]
            for model in get_permitted_models(ml_task)["models"]
            if ("explainable" in model["groups"]) or ("fast" in model["groups"]) or ("advanced" in model["groups"])
        ]

        trial_conf = TrialConfig.with_models(
            task=ml_task, loss_funcs=loss_funcs, models=models, budget_mode=BudgetMode.fast
        )
        return trial_conf

    def get_model_metric_details(self, model: Model) -> List[dict]:
        """
        Get the average metrics for a model in the trial.
        """
        model_details = []
        model_name = model.model_rep.name
        for metric_name, metric_details in model.model_rep.metrics.items():
            for scope, stats in metric_details.items():
                if stats is not None:
                    model_details.append(
                        {"model": model_name, "metric": metric_name, "scope": scope, "average": stats["average"]}
                    )
        return model_details

    def get_metrics_dataframe(self) -> pd.DataFrame:
        """
        Generate a metrics dataframe from a trial object.

        Returns:
            A pandas DataFrame containing the average metrics, pivoted by model, scope, and metric.
        """
        models = self.get_models()
        metrics_list = []
        for model in models:
            metrics_list.extend(self.get_model_metric_details(model))

        # Convert the list of metrics into a DataFrame and pivot
        metrics_df = pd.DataFrame(metrics_list).pivot_table(
            index="model", columns=["metric", "scope"], values="average"
        )

        return metrics_df

    def get_metrics_dataframe_by_model(self, model: Model) -> pd.DataFrame:
        """
        Generate a metrics dataframe from a specific model of the trial.

        Returns:
            A pandas DataFrame containing the average metrics, pivoted by model, scope, and metric.
        """
        metrics_list = [self.get_model_metric_details(model)]

        # Convert the list of metrics into a DataFrame and pivot
        metrics_df = pd.DataFrame(metrics_list).pivot_table(
            index="model", columns=["metric", "scope"], values="average"
        )

        return metrics_df


# ─────────────────────────────── AUTOML METHOD ────────────────────────────── #
def automl(
    data: Union[Dataset, pd.DataFrame, np.ndarray, Tuple[np.ndarray, np.ndarray]],
    target_col: Union[int, str],
) -> Model:
    """
    Given a dataset and a target column, return the optimal model
    for that column. This is BLOCKING, any issues will result in
    exceptions being raised.
    """

    # ────────────────────────── Build the dataset ─────────────────────────── #
    data_name = "automl_{}".format(uuid.uuid4().hex)
    if isinstance(data, pd.DataFrame):
        dataset = Dataset.from_pandas(data=data, name=data_name)
    elif isinstance(data, np.ndarray):
        dataset = Dataset.from_numpy(data=data, name=data_name)
    elif isinstance(data, tuple) and isinstance(data[0], np.ndarray) and isinstance(data[0], np.ndarray):
        dataset = Dataset.from_numpy_xy(data_x=data[0], data_y=data[1], name=data_name)
    else:
        dataset = data
    if dataset.get_state() == DatasetState.OFFLINE:
        dataset.put()
    print("Dataset Uploaded - {}".format(dataset.url))
    dataset.wait()
    print("Dataset Analysed - {}".format(dataset.url + "?activeTab=features"))
    if isinstance(target_col, str):
        target_col_indx = dataset._find_column_by_name(target_col)
    else:
        target_col_indx = target_col
    # ────────────────────── Identify Task and Loss Func ───────────────────── #
    trial_conf = Trial._infer_config(dataset=dataset, target_col_index=target_col_indx)

    # ────────────────────────── Build & Run Trial  ────────────────────────── #
    trial, _ = Trial.from_dataset(
        dataset=dataset,
        trial_name="automl_{}".format(uuid.uuid4().hex),
        target_col=target_col_indx,
        config=trial_conf,
    )
    trial.put()
    trial.start()
    print("Trial Started - {}".format(trial.url))
    trial.wait()
    print("Trial Complete - {}".format(trial.url + "?activeTab=ml-models"))

    # ───────────────────────── Return the best model ──────────────────────── #
    best_model = trial.get_best()
    best_model.build_model()
    return best_model
