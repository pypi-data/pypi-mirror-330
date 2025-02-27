# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations
from typing import Dict, List, Tuple, Union, Optional, Any
from pathlib import Path

from loguru import logger

from evoml_client.api_calls import (
    get_permitted_models,
    get_loss_funcs,
    find_loss_func,
    get_budget,
    get_transformation_options,
    get_default_models,
)

from evoml_client.trial_conf_models import (
    FeatureDimensionalityReductionOptions,
    MlTask,
    BudgetMode,
    OversamplingOptions,
    OversamplingStrategyEnum,
    TrialOptions,
    SplitMethodOptions,
    FeatureGenerationOptions,
    ValidationMethodOptions,
    ValidationMethod,
    HoldoutOptions,
    CrossValidationOptions,
    FeatureSelectionOptions,
    SelectionMethod,
    RedundancyMetric,
    RedundancyAggregation,
    ImportanceOptions,
    MRMROptions,
    TransformationOption,
    Optimizer,
    TimeseriesOptions,
)

try:
    from metaml.meta_models.names import ModelNameType
except ImportError:
    from typing import TypeVar

    ModelNameType = TypeVar("ModelNameType")
    logger.info(
        "metaml package not found. Using generic type hint for ModelNameType. "
        "This won't affect functionality but may reduce type checking capabilities."
    )


# ──────────────────────────────────────────────────────────────────────────── #


# ───────────────────────────────── Helpers ────────────────────────────────── #
def get_allowed_models(task: MlTask) -> List[str]:
    result = [model["name"] for model in get_permitted_models(task)["models"]]
    return result


def get_allowed_loss_funcs(task: MlTask) -> List[Tuple[str, str]]:
    result = [(lf["name"], lf["description"]) for lf in get_loss_funcs(task)]
    return result


def get_allowed_metaml_models() -> List[str]:
    try:
        from metaml import ClassifierName, RegressorName, ForecasterName

    except ImportError:
        logger.info(
            (
                "Model validation couldn't take place because evoml-client is installed. "
                "Please install evoml-client[full] which allow further validations. "
                "Continuing without applying strict validations on models."
            )
        )

    models_names = (
        [prop.value for prop in ClassifierName]
        + [prop.value for prop in RegressorName]
        + [prop.value for prop in ForecasterName]
    )

    return models_names


# ──────────────────────────────────────────────────────────────────────────── #


class TrialConfig:
    """
    USAGE MODES:
        Default         -- user specs: target column, class or regress, num evals, loss_func
        Limited Models  -- Above + user specs: model names & optionally model params
        DataParams      -- Above + user specs: data splitting and validation params
        Full            -- user specs: everything, nothing assumed
        -- All usage modes will generate the full config json and save for user inspection --
    ACTIONS:
        init(target, task, num_eval, loss_funcs)    -- Default mode
        init(Default + model type)                  -- Limited Models mode
        init(Default + model names)                 -- Limited Models mode
        init(above + optional[model params])        -- Limited Models mode
        init(above + split & validation params)     -- Data params mode
        init(config_file)                           -- Full config mode
        dict()                                      -- generate full trial config dict
        json()                                      -- generate full trial config json
    """

    # ──────────────────────────── Constructors ────────────────────────────── #
    def __init__(self, options: Optional[TrialOptions] = None):
        self.options = options or TrialOptions()

    @classmethod
    def with_default(
        cls,
        task: MlTask,
        budget_mode: BudgetMode,
        loss_funcs: Union[List[str], str],
        dataset_id: str = None,
        is_timeseries: bool = False,
        timeseries_column_index: int = 0,
        timeseries_horizon: int = 1,
        timeseries_window_size: int = 5,
    ) -> TrialConfig:
        """
        Given:
            task - either regression or classification
            budget_mode - fast / normal / slow, decides how many trials to run
            loss_funcs - list of names of loss functions to use
            (see get_allowed_loss_funcs(task))
            dataset_id - id of dataset, used to retrieve transformation options
            is_timeseries - whether the dataset is a timeseries
            timeseries_column_index - timeseries index to identify timeseries column
            timeseries_horizon - time gap between the lags and the target
        Returns: TrialConfig object, with sensible defaults for other
        more complex settings
        """
        if timeseries_horizon not in range(1, 101) or (timeseries_horizon != 1 and task == MlTask.forecasting):
            raise ValueError("timeseries_horizon must be 1 for forecasting, otherwise between 1 and 100 inclusive.")
        trial_conf = cls()
        loss_funcs = [loss_funcs] if isinstance(loss_funcs, str) else loss_funcs
        trial_conf.options.mlTask = task
        trial_conf.options.optimizerName = Optimizer.tpe
        trial_conf.options.columnsOptions = []
        trial_conf.options.splittingMethodOptions = SplitMethodOptions(method="percentage", trainPercentage=0.76)
        trial_conf.options.featureGenerationOptions = FeatureGenerationOptions(enable=False)
        trial_conf.options.featureDimensionalityReductionOptions = FeatureDimensionalityReductionOptions(enable=False)
        if task == MlTask.forecasting:
            trial_conf.options.isTimeSeries = True
            trial_conf.options.timeSeriesColumnIndex = timeseries_column_index
            trial_conf.options.timeSeriesHorizon = 1
            trial_conf.options.timeSeriesGenerateLags = True
            trial_conf.options.validationMethodOptions = ValidationMethodOptions(
                method=ValidationMethod.holdout, holdoutOptions=HoldoutOptions(keepOrder=False, size=0.2)
            )
        else:
            if is_timeseries:
                trial_conf.options.isTimeSeries = True
                trial_conf.options.timeSeriesHorizon = timeseries_horizon if task != MlTask.forecasting else 1
                trial_conf.options.timeSeriesColumnIndex = timeseries_column_index
                trial_conf.options.timeSeriesGenerateLags = True
                trial_conf.options.validationMethodOptions = ValidationMethodOptions(
                    method=ValidationMethod.holdout, holdoutOptions=HoldoutOptions(keepOrder=False, size=0.2)
                )
            else:
                trial_conf.options.isTimeSeries = False
                trial_conf.options.validationMethodOptions = ValidationMethodOptions(
                    method=ValidationMethod.cross_validation,
                    crossValidationOptions=CrossValidationOptions(folds=5, keepOrder=False),
                )
        trial_conf.options.transformationOptions = get_transformation_options(dataset_id)
        trial_conf.options.featureSelectionOptions = FeatureSelectionOptions(
            enable=False,
            noOfFeatures=None,
            selectionMethod=SelectionMethod.mrmrimportance,
            relevancyMetrics=["f-test"],
            redundancyMetric=RedundancyMetric.pearson,
            redundancyAggregation=RedundancyAggregation.mean,
            enableSequential=False,
            importanceOptions=ImportanceOptions(),
            mrmrOptions=MRMROptions(),
        )

        trial_conf.options.lossFunctionsIds = [find_loss_func(l_func, task) for l_func in loss_funcs]

        trial_conf.options.models = get_default_models(task)

        trial_conf.budgetAllocationMode = budget_mode
        trial_conf.budget = get_budget(allocation_mode=budget_mode, models=trial_conf.options.models)
        trial_conf.includeGreenMetrics = False
        trial_conf.options.timeSeriesWindowSize = timeseries_window_size
        trial_conf.options.seed = 2027
        trial_conf.options.selectedPositiveLabel = None
        trial_conf.options.enableBudgetEnsemble = True
        trial_conf.options.enableBudgetTuning = True

        trial_conf.options.oversampling = OversamplingOptions(strategy=OversamplingStrategyEnum.NoStrategy, ratio=None)

        return trial_conf

    @classmethod
    def with_models(
        cls,
        task: MlTask,
        budget_mode: BudgetMode,
        loss_funcs: Union[List[str], str],
        models: List[Union[ModelNameType.value, Dict[ModelNameType.value, Dict[str, Any]]]],
        dataset_id: str = None,
        is_timeseries: bool = False,
        timeseries_column_index: int = 0,
        timeseries_horizon: int = 1,
        timeseries_window_size: int = 5,
    ):
        """
        Given:
            task - either regression or classification
            budget_mode - fast, normal, slow -- how thoroughly to search for models
            loss_funcs - list of names of loss functions to use
            (see get_allowed_loss_funcs(task))
            models - either a list of model names (see get_allowed_models(task)),
            or, a List of Dicts of the structure:\n\n
            [{model_name:{param_name: [param option, param option],
            param_name: {"min":param val, "max":param val},
            param_name: param val}}]
            dataset_id - id of dataset, used to retrieve transformation options
            is_timeseries - whether the dataset is a timeseries
            timeseries_column_index - timeseries index to identify timeseries column
            timeseries_horizon - time gap between the lags and the target
        Returns: TrialConfig object, with sensible defaults for other
        more complex settings
        """
        model_params_present = all(isinstance(item, dict) for item in models)
        trial_conf = cls.with_default(
            task=task,
            budget_mode=budget_mode,
            loss_funcs=loss_funcs,
            dataset_id=dataset_id,
            is_timeseries=is_timeseries,
            timeseries_column_index=timeseries_column_index,
            timeseries_horizon=timeseries_horizon,
            timeseries_window_size=timeseries_window_size,
        )
        all_models = get_permitted_models(task)["models"]

        if model_params_present:
            trial_conf.options.models = []
            for model in models:
                model_name = list(model.keys())[0]
                model_rep = next(
                    (item for item in all_models if item["name"] == model_name),
                    None,
                )
                if model_rep is None:
                    continue

                for param in list(model[model_name].keys()):
                    param_rep = next(
                        (item for item in model_rep["parameters"]["inputParameters"] if item["parameterName"] == param),
                        None,
                    )
                    if param_rep is None:
                        continue

                    if isinstance(model[model_name][param], list):
                        # A list of options has been given
                        param_rep["values"] = model[model_name][param]
                    elif isinstance(model[model_name][param], dict):
                        # A dict of min and max has been given
                        param_rep["maxValue"] = model[model_name][param]["max"]
                        param_rep["minValue"] = model[model_name][param]["min"]
                    elif isinstance(model[model_name][param], (float, int, str)):
                        # A default value set explicitly
                        param_rep["defaultValue"] = model[model_name][param]
                        if param_rep["parameterType"] in ["float", "int"]:
                            param_rep["maxValue"] = model[model_name][param]
                            param_rep["minValue"] = model[model_name][param]
                    else:
                        continue
                trial_conf.options.models.append(model_rep)
        else:
            allowed_models_names = get_allowed_metaml_models()

            for model in models:
                if model not in allowed_models_names:
                    raise ValueError("Models must belong to ClassifierName, RegressorName or ForecasterName")

            trial_conf.options.models = [model for model in all_models if model["name"] in models]
        return trial_conf

    @classmethod
    def with_model_type(
        cls,
        task: MlTask,
        model_type: str,
        budget_mode: BudgetMode,
        loss_funcs: Union[List[str], str],
        is_timeseries: bool = False,
        timeseries_column_index: int = 0,
        timeseries_horizon: int = 1,
    ):
        """
        Given:
            task - either: regression or classification
            model_type - either: fast, explainable or advanced
            budget_mode - fast, normal, slow -- how thoroughly to search for models
            loss_funcs - list of names of loss functions to use
            (see get_allowed_loss_funcs(task))
            is_timeseries - whether the dataset is a timeseries
            timeseries_column_index - timeseries index to identify timeseries column
            timeseries_horizon - time gap between the lags and the target
        Returns: TrialConfig object, with sensible defaults for other
        more complex settings
        """
        models = [model["name"] for model in get_permitted_models(task)["models"] if (model_type in model["groups"])]
        return cls.with_models(
            task=task,
            budget_mode=budget_mode,
            loss_funcs=loss_funcs,
            models=models,
            is_timeseries=is_timeseries,
            timeseries_column_index=timeseries_column_index,
            timeseries_horizon=timeseries_horizon,
        )

    @classmethod
    def with_data_params(
        cls,
        task: MlTask,
        budget_mode: BudgetMode,
        loss_funcs: List[str],
        models: List[Union[ModelNameType.value, Dict[ModelNameType.value, Dict[str, Any]]]] = [],
        dataset_id: str = None,
        timeseries_options: TimeseriesOptions = None,
        split_options: SplitMethodOptions = None,
        valid_options: ValidationMethodOptions = None,
        feature_gen_options: FeatureGenerationOptions = None,
        feature_sel_options: FeatureSelectionOptions = None,
        trans_options: List[TransformationOption] = None,
    ) -> TrialConfig:
        """
        Given:
            task - either regression or classification
            loss_funcs - list of names of loss functions to use
            (see get_allowed_loss_funcs(task))
            models - either a list of model names (see get_allowed_models(task)),
            or, a List of Dicts of the structure:
            [{model_name: {param_name: param val, param_name: param val, ...}}, ...]
            is_timeseries - whether the dataset is a timeseries
            timeseries_column_index - timeseries index to identify timeseries column
            timeseries_horizon - time gap between the lags and the target
            split_options: a SplitMethodOptions object to store parameters
            for train test splitting
            valid_options: a ValidationMethodOptions object to store parameters
            for how models should be validated
        Returns: TrialConfig object, with sensible defaults for other
        more complex settings
        """
        permitted_models = [
            model["name"] for model in get_permitted_models(task)["models"] if (model["enabled"] is True)
        ]
        for model in models:
            if model not in permitted_models:
                raise Exception(
                    f"Input model {model} is not managed by the Evoml platform."
                    f" The list of permitted models are: {permitted_models}"
                )
        timeseries_options = TimeseriesOptions(is_timeseries=False) if not timeseries_options else timeseries_options
        trial_conf = cls.with_models(
            task=task,
            budget_mode=budget_mode,
            loss_funcs=loss_funcs,
            models=models,
            dataset_id=dataset_id,
            is_timeseries=timeseries_options.is_timeseries,
            timeseries_column_index=timeseries_options.column_index,
            timeseries_horizon=timeseries_options.horizon,
            timeseries_window_size=timeseries_options.window_size,
        )
        trial_conf.options.columnsOptions = []
        if not trial_conf.options.models:
            trial_conf.options.models = get_default_models(task)

        # If the user provided some configuration it is substituted from the defaults
        if split_options is not None:
            trial_conf.options.splittingMethodOptions = split_options

        if valid_options is not None:
            trial_conf.options.validationMethodOptions = valid_options

        if feature_gen_options is not None:
            trial_conf.options.featureGenerationOptions = feature_gen_options

        if feature_sel_options is not None:
            trial_conf.options.featureSelectionOptions = feature_sel_options

        if trans_options is not None:
            trial_conf.options.transformationOptions = trans_options

        return trial_conf

    @classmethod
    def with_param_file(cls, config_file: Path) -> TrialConfig:
        """
        Given a json containing a full trial config return a
        TrialConfig object
        """
        trial_conf = cls(options=TrialOptions.parse_file(config_file))
        return trial_conf

    @classmethod
    def with_params(cls, config_json: Dict) -> TrialConfig:
        """
        Given a dict containing a full trial config, return a
        TrialConfig object
        """
        trial_conf = cls(options=TrialOptions(**config_json))
        return trial_conf

    # ──────────────────────── Config Generation ───────────────────────────── #
    def json(self) -> str:
        """returns the Full trial config as a json"""
        return self.options.json()

    def dict(self) -> dict:
        """returns the full trial config as a json"""
        return self.options.dict()
