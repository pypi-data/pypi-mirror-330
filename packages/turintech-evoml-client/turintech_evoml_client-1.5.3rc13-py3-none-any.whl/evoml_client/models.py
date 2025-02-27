from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel


class Status(str, Enum):
    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REQUEUED = "requeued"
    UNKNOWN = "unknown"


class Type(str, Enum):
    DETECT = "detect"
    PREPROCESS = "preprocess"
    VISUALISE = "visualise"
    GENERATE_API_GRAPHS = "generate-ai-graphs"
    EVOML = "evoml"
    DEPLOY = "deploy"
    UPLOAD = "upload"
    UNKNOWN = "unknown"


class Task(BaseModel):
    externalId: str
    type: Type
    status: Status
    progress: int
    startedAt: Optional[datetime]
    finishedAt: Optional[datetime]


class NamedValue(BaseModel):
    name: str
    value: str


class Stage(BaseModel):
    name: str
    index: int


class MetricsValues(BaseModel):
    values: List[float]
    min: float
    max: float
    average: float
    median: float


class Metrics(BaseModel):
    train: Optional[MetricsValues]
    validation: MetricsValues
    test: Optional[MetricsValues]


class PipelineLog(BaseModel):
    message: str
    level: str
    timestamp: datetime


class Pipeline(BaseModel):
    _id: str
    id: str
    trialId: Optional[str]
    name: str
    mlModelName: str
    scores: dict
    metrics: Optional[Dict[str, Metrics]]
    representation: Optional[str]
    graph: Optional[dict]
    parameters: Optional[List[NamedValue]]
    stage: Optional[Stage]
    log: Optional[PipelineLog]
    notes: Optional[List[NamedValue]]
    totalTrainingTime: Optional[float]
    totalPredictionTime: Optional[float]
    gpus: int
    cpus: int
    ramInBytes: int
    status: Status = Status.SUCCESS
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    producedAt: Optional[datetime]
    deleted: bool = False


class Order(str, Enum):
    ASC = "asc"
    DESC = "desc"


class Objective(BaseModel):
    name: str
    slug: str
    order: Order


class ToggledGraph(BaseModel):
    title: str
    graphId: str
    alternativeGraphId: Optional[str]
    toggleButtonText: Optional[str]


class NamedGraph(BaseModel):
    title: str
    graphId: str


class NamedImageFile(BaseModel):
    title: str
    fileId: str
    description: str


class ImageGroup(BaseModel):
    title: str
    images: Optional[List[NamedImageFile]]


class PipelineReport(BaseModel):
    mlTask: str
    pipelineId: str
    pipelineZipFileId: Optional[str]
    pipelineHandlerFileId: Optional[str]
    predictionCsvFileId: Optional[str]
    metrics: Optional[Dict[str, Metrics]]


class ProcessInfo(BaseModel):
    _id: str
    externalId: str
    status: Status
    progress: int
    startedAt: Optional[datetime]
    finishedAt: Optional[datetime]
    executionTime: Optional[int]
    createdAt: datetime
    updatedAt: datetime
    tasks: List[Task]
