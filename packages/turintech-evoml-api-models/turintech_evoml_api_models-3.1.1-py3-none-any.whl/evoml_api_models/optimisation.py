"""Models used by optimisation components to generate machine learning models
and send the results. It contains the following groups:
- preprocessing infos
- loss functions
"""
# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from typing import List, Dict, Type, Optional, Any, Generic, Union, TypeVar
from enum import Enum

# ---------------------------------------------------------------------------- #
# Dependencies
import numpy as np
from pydantic.v1 import (
    BaseModel,
    ValidationError,
    Field,
    StrictFloat,
    StrictInt,
    StrictStr,
    validator
)
from pydantic.v1.generics import GenericModel

# ---------------------------------------------------------------------------- #
# Module
from .utils import use_alias
from .graphs import (
    Histogram,
    ScatterPlot,
    BarChart,
    ConfusionMatrix,
    BoxPlot,
    MultiClassROCCurve,
    MultiClassPrecisionRecallCurve,
    LineHistogram,
    LineGraph,
    Graph,
    GraphT,
)
# ──────────────────────────────────────────────────────────────────────────── #
class MlTask(str, Enum):
    """Enum of the different types of machine larning problems/tasks
    """
    regression = "regression"
    classification = "classification"
    forecasting = "forecasting"

# ───────────────────────────────── metadata ───────────────────────────────── #
# config.json --> informations about the dataset
class DatasetMetadata(BaseModel):
    """Dataset metadata: informations about a dataset uploaded on enigma's
    database
    """
    rowsCount: int = Field(None, example=2340)
    columnsCount: int = Field(None, example=2340)
    encoding: Optional[str] = None
    delimiter: Optional[str] = None


# config.json / config.json --> informations about the preprocessed dataset
class PreprocessedMetadata(BaseModel):
    """Metadata about a preprocessed file"""
    # For classification, labelMappings is a list of strings,
    # for regression, labelMappings is a list of mixed int and floats.
    labelMappings: Optional[Union[List[Union[StrictFloat, StrictInt]], List[StrictStr]]]
    futureCovariates: List[str] = []


# ──────────────────────── statistics / column-infos ───────────────────────── #
# types.json --> informations about the type & anomalies of each column
class GeoLocationType(str, Enum):
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    LAT_LONG = "latLong"


class CategoricalMetadata(BaseModel):
    """Metadata for the categorical detected type"""
    isSpecialCategorical: bool = False


class GeoLocationMetadata(BaseModel):
    """Metadata for the geoLocation detected type"""
    geographicalCoordinate: GeoLocationType


class DateTimeMetadata(BaseModel):
    """Metadata for the dateTime detected type"""
    dateTimeOrder: str


class UnitNumberMetadata(BaseModel):
    """Metadata for the unitNumber detected type"""
    unit: str


class BankCodeMetadata(BaseModel):
    """Metadata for the bankCode detected type"""
    type: str


class BarCodeMetadata(BaseModel):
    """Metadata for the barcode detected type"""
    type: str


class CurrencyMetadata(BaseModel):
    """Metadata for the currency detected type"""
    majorityCurrency: str
    allCurrencies: List[str]


class PhoneNumberMetadata(BaseModel):
    """Metadata for the phoneNumber detected type"""
    country: Optional[str]


class DetectedType(str, Enum):
    """List of types that can be detected for a column of a dataset"""
    integer = "basicInteger"
    float = "basicFloat"
    unary = "unary"
    binary = "binary"
    datetime = "dateTime", DateTimeMetadata
    categorical = "categorical", CategoricalMetadata
    text = "text"
    url = "url"
    currency = "currency", CurrencyMetadata
    email = "email"
    fraction = "fraction"
    geo_location = "geoLocation", GeoLocationMetadata
    ip = "ipAddress"
    percentage = "percentage"
    phone = "phoneNumber", PhoneNumberMetadata
    unit_number = "unitNumber", UnitNumberMetadata
    address = "address"
    list = "list"
    map = "map"
    barcode = "barcode", BarCodeMetadata
    bank_code = "bankCode", BankCodeMetadata
    protein_sequence = "proteinSequence"
    sample_id = "ID"
    duplicate = "duplicate"
    unsupported = "unsupported"
    unknown = "unknown"

    # Generic setting to allow association of {type -> metadata_class}
    metadata_model: Optional[Type[BaseModel]]

    def __new__(cls, name: str, model_class: Optional[Type[BaseModel]] = None):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj.metadata_model = model_class
        return obj

    def validate_metadata(self, metadata: Union[BaseModel, dict, None]) -> bool:
        """Validates a metadata model or dictionary for this detected type
        (does this match the expected format of metadata).
        """
        # Everything is valid if we don't need metadata
        if self.metadata_model is None:
            return True

        # If we're a model, we need to be of the right class
        if isinstance(metadata, BaseModel):
            return isinstance(metadata, self.metadata_model)

        try:
            self.metadata_model.parse_obj(metadata)
        except ValidationError:
            return False
        return True


DetectedTypeMetadata = TypeVar(
    "DetectedTypeMetadata", *set([dtype.metadata_model for dtype in list(DetectedType)])
)


class BaseTypes(str, Enum):
    """List of basetypes that can be detected for a column of a dataset"""
    string = "string"
    float = "float"
    integer = "int"
    unknown = "unknown"

class ColumnAnomalies(BaseModel):
    """Anomalies found inside a column of the dataset, showing which lines are
    considered anomalies.
    """
    lines: List[int]


class ColumnStatistics(BaseModel):
    """A single statistic about a column's data
    """
    name: str = Field(..., example="missing_rate")
    value: str = Field(..., example="0.1")
    description: str = Field(..., example="Missing rate")


class ColumnTag(BaseModel):
    """A single tag providing information to the user about a column's data
    (different from statistics)
    """
    slug: str = Field(..., example="missing_rate")
    # actual string to display on the frontend
    name: str = Field(..., example="low missing rate")
    # tooltip
    description: str = Field(..., example="The missing rate is 20%")
    # can be used to control the color of the tag
    severity: float = Field(..., example=3.5)


class ColumnDefaultTrialOptions(BaseModel):
    isValidTarget: bool = Field(False)
    mlTask: MlTask = Field(..., example="classification")
    lossFunctionSlugs: List[str] = Field(..., example=["classification-accuracy"])
    onSelectAsTargetMessage: Optional[str] = None
    onMlTaskChangedMessage: Optional[str] = None
    isBinaryClassification: Optional[bool] = False
    binaryLabels: List[str] = []


class GenericColumnStatistics(BaseModel):
    statsUniqueValuesRatio: float = Field(..., example=0.1)
    statsUniqueValuesCount: int = Field(..., example=100)
    statsMissingValuesRatio: float = Field(..., example=0.1)
    statsMissingValuesCount: int = Field(..., example=100)
    statsValuesCount: int = Field(..., example=1000)


class QuickColumnInfo(BaseModel):
    # used in quick mode of type detector
    columnIndex: int = Field(..., example=7)
    name: str = Field(..., example="column 7")
    baseType: BaseTypes = Field(..., example="string")


class BaseColumnInfo(QuickColumnInfo):
    # Core components of the column info, all required
    # -> Intermediate level
    detectedType: DetectedType = Field(..., example="integer")
    confidenceScore: float = Field(..., example=1.0)
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="information to be used by the preprocessor"
    )


    @validator('metadata')
    def sanitize_metadata(cls, metadata: Optional[dict]) -> Optional[dict]:
        """Make sure that the `metadata` field does not contain any numpy array
        structures
        """
        if metadata is None:
            return
        for key, value in metadata.items():
            if isinstance(value, np.ndarray):
                metadata[key] = value.tolist()
        return metadata


class ColumnInfo(BaseColumnInfo, GenericColumnStatistics):
    """Model gathering all information and statistics about a single column of
    a dataset, generated suring the dataset analysis step.
    This model is used to register a column's info in the database.
    """
    # More advanced components, all optionals and/or empty default values
    defaultTrialOptions: Optional[ColumnDefaultTrialOptions] = None
    statistics: List[ColumnStatistics] = []
    tags: List[ColumnTag] = []
    anomalies: Optional[ColumnAnomalies] = None
    isDeleted: bool = False


class PreprocessSingleColumnStatistics(BaseModel):
    colName: str
    detectedType: Optional[str]
    scaler: str
    encoder: str
    imputeCount: int
    columnNamesAfterEncoding: List[str]
    # The uniqueLabel field is only for those that have been
    # Label Encoded
    uniqueLabels: Optional[Any]

class GeneratedFeature(BaseModel):
    generatedFeatureName: str
    formula: str
    ast:Dict[Any, Any]
    featuresUsed: List[str]
    basisFunctions: List[str]

class PreprocessFeatureSelectionReport(BaseModel):
    selectedFeatureNamesAfterEncoding: List[str]
    lowVarianceColumnsRemoved: int
    lowVariancePercentCutoff: float
    totalCorrelatedColumnsDropped: int
    correlationMethod: str
    correlationThreshold: float
    columnsCorrelatedWithLabelColumn: List[str]
    columnsDroppedFromFeatureSelection: List[str]
    stageOneFeatureSelectionMethods: List[str]
    stageTwoFeatureSelectionMethods: List[str]
    
class PreprocessFeatureGenerationReport(BaseModel):
    featuresGenerated: List[GeneratedFeature]

class PreprocessMultiColumnStatistics(BaseModel):
    featureSelectionReportGenerated: bool
    featureSelectionReport: Optional[PreprocessFeatureSelectionReport]
    featureGenerationReportGenerated: bool
    featureGenerationReport: Optional[PreprocessFeatureGenerationReport]
    columnCountBeforePreprocessing: int
    columnCountAfterPreprocessing: int
    droppedRows: int
    droppedColumns: List[str]

class PreprocessReport(BaseModel):
    multiColumnStatistics: PreprocessMultiColumnStatistics
    singleColumnStatistics: List[PreprocessSingleColumnStatistics]
    totalPreprocessingTime: float


# ────────────────────────────── loss functions ────────────────────────────── #
class LossFunction(BaseModel):
    """Loss function used to parametrize an optimisation task"""
    name: str
    isCustom: bool
    mlTask: MlTask
    order: str
    sourceCode: Optional[str]
    slug: str

# ──────────────────────────── feature importance ──────────────────────────── #


class FeatureImportance(BaseModel):
    """Model defining the importance of each individual features"""
    name: str = Field(..., description="Name of the feature")
    importance: float
    error: Optional[float] = None


class ModelFeatureImportances(BaseModel):
    """Model defining for the feature importances of a single model"""
    # This name indicates what this specific feature importance represents. If
    # there's a single feature importance, it doesn't matter much.
    # If there's multiple of them, it gives context on what each one means.
    # See `EnsembleFeatureImportances` for more details
    name: Optional[str] = Field(
        None,
        example="Tree 1",
        description="Name of this feature importance. It should not be None if "
        "there's 2 or more feature importances in an ensemble",
    )
    features: List[FeatureImportance] = Field(..., min_items=1)
    intercept: Optional[List[float]] = Field(
        None,
        description="Intercept for linear regressions, to use in the equation for prediction",
    )
    totalFeatures: int = Field(None, description="Total number of available features")


    @validator('totalFeatures', always=True)  # Trigger for default value
    def set_total_features(cls, _, values: dict):
        """The total number of features is the length of the list of features
        when the model is first instanciated. This value is here in case a call
        to `set_max_features` is done to keep track of the actual max number.
        """
        features: list = values.get("features", [])
        return len(features)


    def set_max_features(self, max_features: Optional[int] = None):
        """Limits the number of received feature importances to the first
        `max_features` elements.
        """
        if max_features is None or len(self.features) <= max_features:
            return

        get_score = lambda feature: abs(feature.importance)
        sorted_features = list(sorted(self.features, key=get_score))
        self.features = sorted_features[:max_features]


class EnsembleFeatureImportances(BaseModel):
    """Model providing the data for a generic feature importance that supports
    ensemble models (e.g. Random Forest) with multiple submodels each having its
    own feature importance data
    """
    featureImportances: List[ModelFeatureImportances]


    @validator('featureImportances')
    def ensure_name(cls, feature_importances: List[ModelFeatureImportances]):
        """An empty name in a feature-importance only makes sense if
        there is no other feature-importance in the ensemble
        """
        if len(feature_importances) > 1:
            # We use `bool(name)` ⇒ name != None && name != ""
            assert all([bool(fi.name) for fi in feature_importances])
        return feature_importances


# ──────────────────────────────────────────────────────────────────────────── #
# ──────────────── Report & Results - Machine learning models ──────────────── #
# Models used to communicate the machine learning models created by an
# optimisation task

class Node(BaseModel):
    """Node of a graph, used by the ReportModel and ResultModel"""
    id: str
    label: str
    type: int
    properties: List[str] = None


class Edge(BaseModel):
    """Edge of a graph, used by the ReportModel and ResultModel"""
    id: str
    label: str
    source: str
    target: str


class MlGraph(BaseModel):
    """A machine learning graph representation, used by the ReportModel and ResultModel"""
    nodes: List[Node]
    edges: List[Edge]


class Order(str, Enum):
    """Directions of optimisation objectives"""
    asc: str = 'asc'
    desc: str = 'desc'


class Objective(BaseModel):
    """Optimisation objective"""
    slug: str
    name: str
    order: Order = Order.desc


class StatsPair(BaseModel):
    name: str
    value: str


class MetricsData(BaseModel):
    values: List[float]
    min: float
    max: float
    average: float
    median: float


class PipelineMetrics(BaseModel):
    train: Optional[MetricsData]
    validation: MetricsData
    test: Optional[MetricsData]


class StageNames(str, Enum):
    FILTERING = "filtering"
    TUNING = "tuning"
    STACKING = "stacking"
    RANDOM_SEARCH = "random-search"
    BEST_MODEL = "best-model"


class Stage(BaseModel):
    name: StageNames
    index: int


@use_alias
class Pipeline(BaseModel):
    """A machine learning pipeline, used by the ReportModel and ResultModel"""
    hash: str = Field(..., alias='id')
    name: str
    mlModelName: str
    graph: MlGraph
    scores: Dict[str, float]
    parameters: Optional[List[StatsPair]]
    notes: Optional[List[StatsPair]]
    metrics: Dict[str, PipelineMetrics]
    stage: Stage
    producedAt: str
    totalTrainingTime: Optional[float] = None
    totalPredictionTime: Optional[float] = None
    featureImportances : Optional[EnsembleFeatureImportances] = None
    totalTrainingTime: Optional[float] = Field(
        None, description="Total time to fit the model on the train data"
    )
    totalPredictionTime: Optional[float] = Field(None)
    gpus: int = Field(..., description="Maximum number of gpus available for the model")
    cpus: int = Field(..., description="Maximum number of cpus available for the model")
    ramInBytes: int = Field(
        ...,
        description="Maximum quantity of RAM (in bytes) available to train the model",
    )


class Report(BaseModel):
    """Report to communicate intermediate results generated by an optimisation
    component. Contains multiple pipelines, a summary of the best pipelines
    included (ordered).
    Differs from results because it does not include additional information
    about those pipelines, just the pipelines themselve.
    """
    pipelines: Optional[List[Pipeline]]
    objectives: List[Objective]


class NamedGraph(GenericModel, Generic[GraphT]):
    title: str
    graph: Graph[GraphT]


class ToggleGraph(NamedGraph[GraphT], Generic[GraphT]):
    alternativeGraph: Optional[Graph[GraphT]]
    toggleButtonText: Optional[str]


class ImagePath(BaseModel):
    title: str
    description: Optional[str]
    path: str


class ImagePathGroup(BaseModel):
    title: str
    images: List[ImagePath]

__all__ = [
    "BaseColumnInfo",
    "BaseTypes",
    "ColumnAnomalies",
    "ColumnInfo",
    "ColumnStatistics",
    "ColumnDefaultTrialOptions",
    "ColumnTag",
    "DatasetMetadata",
    "DetectedTypeMetadata",
    "DetectedType",
    "Edge",
    "GenericColumnStatistics",
    "LossFunction",
    "MlGraph",
    "MlTask",
    "Node",
    "Objective",
    "Order",
    "StatsPair",
    "MetricsData",
    "Pipeline",
    "PipelineMetrics",
    "PreprocessedMetadata",
    "PreprocessReport",
    "PreprocessSingleColumnStatistics",
    "PreprocessMultiColumnStatistics",
    "QuickColumnInfo",
    "Report",
    "ImagePath",
    "ImagePathGroup",
    "ToggleGraph",
    "NamedGraph",
    "FeatureImportance",
    "ModelFeatureImportances",
    "EnsembleFeatureImportances",
]
