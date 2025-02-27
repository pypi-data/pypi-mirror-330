"""
A collection of pydantic models to represent and validate trial configuration
SECTIONS:
    ML Model         -- Used to build the nested structure for trial models
    Data Control     -- Exposes how train and test data will be divided
    Top lvl Concepts -- Enum and top lvl model to contain the conf tree
"""

# ───────────────────────────────── imports ────────────────────────────────── #
from typing import List, Any, Dict, Optional, Union, Type
from enum import Enum

from evoml_api_models import BaseModelWithAlias
from pydantic import BaseModel, Field, StrictInt

from evoml_client.trial_conf_detection_types import (
    EncoderType,
    Scaler,
    BasicIntegerEncoders,
    BasicFloatEncoders,
    CurrencyEncoders,
    FractionEncoders,
    PercentageEncoders,
    UnitNumberEncoders,
    TextEncoders,
    ProteinSequenceEncoders,
    BinaryEncoders,
    CategoricalEncoders,
)


# ───────────────────────────── ML Model models ────────────────────────────── #
class InputParameter(BaseModel):
    enabled: bool = True
    parameterName: str
    parameterType: str
    fixedValue: Optional[bool] = False
    minValue: Optional[Union[StrictInt, float]] = None
    maxValue: Optional[Union[StrictInt, float]] = None
    values: List[Any]
    defaultValue: Any
    generateDistribution: Optional[str]


class ModelMetadata(BaseModel):
    model: str
    use_default_parameters: bool = True


class ModelParameter(BaseModel):
    inputParameters: List[InputParameter]
    objectivesList: Optional[List[str]]
    metadata: Optional[ModelMetadata]


class ModelConfig(BaseModel):
    name: str
    mlTask: str
    parameters: ModelParameter
    enabled: bool = True
    groups: Optional[List[str]]


# ─────────────────────────── Data Control models ──────────────────────────── #
class CovariatesOptions(str, Enum):
    """Covariates options for feature generation"""

    PAST = "past"
    FUTURE = "future"


class ValidationMethod(str, Enum):
    cross_validation = "cross-validation"
    holdout = "holdout"


class CrossValidationOptions(BaseModel):
    """Cross validation option"""

    folds: int
    keepOrder: bool


class ExpandingWindowOptions(BaseModel):
    """Expanding window options for Holdout validation method."""

    expansionLength: Optional[int]
    gap: int
    horizon: Optional[int]
    initialTrainWindowLength: Optional[int]


class ForecastHoldoutOptions(BaseModel):
    """Forecast holdout options for Holdout validation method."""

    gap: int
    horizon: Optional[int]


class HoldoutOptions(BaseModel):
    """Holdout options for Holdout validation method."""

    keepOrder: bool
    size: float


class SlidingWindowOptions(BaseModel):
    """Expanding window options parameters for Holdout validation method."""

    gap: int
    horizon: Optional[int]
    slideLength: Optional[int]
    trainWindowLength: Optional[int]


class ValidationMethodOptions(BaseModel):
    """Represents settings for either K-folds or holdout validation"""

    crossValidationOptions: Optional[CrossValidationOptions]
    expandingWindowOptions: Optional[ExpandingWindowOptions]
    forecastHoldoutOptions: Optional[ForecastHoldoutOptions]
    holdoutOptions: Optional[HoldoutOptions]
    slidingWindowOptions: Optional[SlidingWindowOptions]
    method: ValidationMethod = ValidationMethod.cross_validation


class OversamplingStrategyEnum(str, Enum):
    NoStrategy = "none"
    Auto = "auto"
    Smote = "smote"
    BorderlineSmote = "borderline-smote"
    SmoteTomek = "smote-tomek"
    SvmSmote = "svm-smote"
    Adasyn = "adasyn"
    RandomOversampling = "random-oversampling"


class OversamplingOptions(BaseModel):
    strategy: OversamplingStrategyEnum = OversamplingStrategyEnum.NoStrategy
    ratio: float = Field(None, gt=0, le=1)


class SplitMethod(str, Enum):
    percentage = "percentage"
    subset = "subset"
    index = "index"


class ColumnFilter(str, Enum):
    keep = "keep"
    drop = "drop"
    auto = "auto"


class ImputeStrategy(str, Enum):
    constant = "constant"
    mean = "mean"
    median = "median"
    mostFrequent = "most-frequent"
    auto = "auto"


class ColumnDetectedType(str, Enum):
    ADDRESS = "address"
    BANK_CODE = "bankCode"
    BARCODE = "barcode"
    BASIC_FLOAT = "basicFloat"
    BASIC_INTEGER = "basicInteger"
    BINARY = "binary"
    CATEGORICAL = "categorical"
    CURRENCY = "currency"
    DATE_TIME = "dateTime"
    DUPLICATE = "duplicate"
    EMAIL = "email"
    FRACTION = "fraction"
    GEO_LOCATION = "geoLocation"
    ID = "ID"
    IP_ADDRESS = "ipAddress"
    LIST = "list"
    MAP = "map"
    PERCENTAGE = "percentage"
    PHONE_NUMBER = "phoneNumber"
    PROTEIN_SEQUENCE = "proteinSequence"
    TEXT = "text"
    UNARY = "unary"
    UNIT_NUMBER = "unitNumber"
    UNKNOWN = "unknown"
    UNSUPPORTED = "unsupported"
    URL = "url"


column_type_mapping = {
    ColumnDetectedType.BASIC_INTEGER: BasicIntegerEncoders,
    ColumnDetectedType.BASIC_FLOAT: BasicFloatEncoders,
    ColumnDetectedType.CURRENCY: CurrencyEncoders,
    ColumnDetectedType.FRACTION: FractionEncoders,
    ColumnDetectedType.PERCENTAGE: PercentageEncoders,
    ColumnDetectedType.UNIT_NUMBER: UnitNumberEncoders,
    ColumnDetectedType.TEXT: TextEncoders,
    ColumnDetectedType.PROTEIN_SEQUENCE: ProteinSequenceEncoders,
    ColumnDetectedType.BINARY: BinaryEncoders,
    ColumnDetectedType.CATEGORICAL: CategoricalEncoders,
}


class EncoderDetails(BaseModelWithAlias):
    name: ColumnDetectedType
    type: List[EncoderType]


class ScalerDetails(BaseModelWithAlias):
    name: ColumnDetectedType
    type: List[Scaler]


class FeatureOverrides(BaseModelWithAlias):
    column_index: int
    encoder_details: EncoderDetails
    scaler_details: ScalerDetails
    covariate: CovariatesOptions = CovariatesOptions.PAST
    filter: ColumnFilter = ColumnFilter.auto


class SelectionMethod(str, Enum):
    mrmr = "mrmr"
    filter = "filter"
    mrmrimportance = "mrmr-importance"


class RedundancyMetric(str, Enum):
    spearman = "spearman"
    pearson = "pearson"
    none = "none"


class RedundancyAggregation(str, Enum):
    mean = "mean"
    max = "max"


class ImportanceAggregation(str, Enum):
    mean = "mean"
    rank = "rank"


class ModelOptions(str, Enum):
    lasso = "lasso-regressor"
    dt = "decision-tree"
    lightgbm = "lightgbm"
    random = "random-forest"
    svm = "support-vector-machine"


class MRMROptions(BaseModel):
    linear: bool = False
    redundancyWeight: int = 0.1
    importanceWeight: int = 0.1


class ImportanceOptions(BaseModel):
    modelOptions: List[ModelOptions] = [ModelOptions.lasso, ModelOptions.dt]
    importanceAggregation: ImportanceAggregation = ImportanceAggregation.rank


class CorrelationMethod(str, Enum):
    cluster = "cluster"
    drop = "drop"
    minRedundancyMaxRelevance = "min-redundancy-max-relevance"
    none = "none"


ImputeValue = Union[StrictInt, float, str]


class Impute(BaseModelWithAlias):
    strategy: ImputeStrategy = ImputeStrategy.auto
    value: Optional[ImputeValue]
    # Union[StrictInt, float, str]


class TimeseriesOptions(BaseModel):
    is_timeseries: bool = True
    column_index: Optional[int] = None
    horizon: int = 1
    window_size: int = 5


class SplitMethodOptions(BaseModel):
    """
    Represents settings for either perc, subset or index data splitting options
    """

    method: SplitMethod = SplitMethod.percentage
    trainPercentage: float = Field(
        0.8,
        gt=0,
        lt=1,
        description="Required for method == 'percentage'",
    )
    subsetColumnName: str = Field(
        None,
        description="Required for method == 'subset'",
        example="city",
    )
    _ranges_description = "for 'index' & 'subset' methods only"
    trainRangeFrom: Any = Field("", description=_ranges_description)
    trainRangeTo: Any = Field("", description=_ranges_description)
    testRangeFrom: Any = Field("", description=_ranges_description)
    testRangeTo: Any = Field("", description=_ranges_description)


EncoderSlugSet: Type[Dict[ColumnDetectedType, List[str]]] = Dict[ColumnDetectedType, Optional[List[str]]]
ScalerSlugSet: Type[Dict[ColumnDetectedType, List[str]]] = Dict[ColumnDetectedType, Optional[List[str]]]


class ColumnTransformationOptions(BaseModel):
    """
    The transformation options for a given column
    """

    columnIndex: int
    filter: ColumnFilter = ColumnFilter.auto
    encoderSlugs: EncoderSlugSet
    scalerSlugs: ScalerSlugSet
    impute: Optional[Impute]
    covariate: CovariatesOptions = CovariatesOptions.PAST


class TransformationOption(BaseModel):
    detectedType: Optional[ColumnDetectedType]
    encoderSlugs: EncoderSlugSet
    scalerSlugs: ScalerSlugSet
    featureOverrides: List[ColumnTransformationOptions]
    impute: Optional[Impute]


class FeatureSelectionOptions(BaseModel):
    enable: bool = False
    noOfFeatures: Optional[int] = 0
    selectionMethod: SelectionMethod = SelectionMethod.mrmr
    relevancyMetrics: List[str] = ["f-test"]
    redundancyMetric: RedundancyMetric = RedundancyMetric.spearman
    redundancyAggregation: RedundancyAggregation = RedundancyAggregation.mean
    enableSequential: bool = True
    importanceOptions: ImportanceOptions
    mrmrOptions: MRMROptions


class DimensionalityReductionMethod(str, Enum):
    SVD = "svd"
    PCA = "pca"
    ICA = "ica"


class FeatureDimensionalityReductionOptions(BaseModel):
    enable: bool = False
    noOfComponents: int = 1
    method: DimensionalityReductionMethod = DimensionalityReductionMethod.SVD


class FeatureGenerationOptions(BaseModel):
    enable: bool = True
    noOfNewFeatures: int = 1
    unaryOps: List[str] = ["sin", "cos"]
    polyOps: List[str] = []
    epochs: int = 1


# ─────────────────────────── Pre-Processor models ─────────────────────────── #


class ColumnGroupTransformationOptions(BaseModel):
    """
    The transformation options for a given column group
    """

    detectedType: ColumnDetectedType
    encoderSlugs: EncoderSlugSet
    scalerSlugs: ScalerSlugSet
    featureOverrides: List[ColumnTransformationOptions]


# ────────────────────────── Top lvl Concept models ────────────────────────── #
class MlTask(str, Enum):
    regression = "regression"
    classification = "classification"
    forecasting = "forecasting"


class Optimizer(str, Enum):
    tpe = "tpe"
    nsgaii = "nsgaii"
    random = "random"


class BudgetMode(str, Enum):
    fast = "fast"
    normal = "normal"
    slow = "slow"


class Budget(BaseModel):
    filtering: int = (0,)
    tuning: int = (0,)
    ensemble: int = 0


class TrialOptions(BaseModel):
    columnsOptions: List = None
    splittingMethodOptions: SplitMethodOptions = None
    validationMethodOptions: ValidationMethodOptions = None
    oversampling: OversamplingOptions = None
    transformationOptions: List[TransformationOption] = None
    featureSelectionOptions: FeatureSelectionOptions = None
    featureGenerationOptions: FeatureGenerationOptions = None
    featureDimensionalityReductionOptions: FeatureDimensionalityReductionOptions = None
    mlTask: MlTask = None
    optimizerName: Optimizer = None
    lossFunctionsIds: List[str] = None
    models: List[ModelConfig] = None
    budgetAllocationMode: BudgetMode = BudgetMode.fast
    budget: Budget = None
    includeGreenMetrics = False  # not needed
    enableBudgetEnsemble: bool = False
    enableBudgetTuning: bool = False
    seed: int = 0
    selectedPositiveLabel: Optional[str] = None
    isTimeSeries: bool = False
    timeSeriesColumnIndex: Optional[int] = None
    timeSeriesWindowSize: Optional[int] = 5
    timeSeriesHorizon: int = 1
    timeSeriesGenerateLags: bool = False
