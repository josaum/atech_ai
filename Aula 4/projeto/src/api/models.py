from typing import List, Dict, Optional
from pydantic import BaseModel


class PredictionData(BaseModel):
    data: dict
    model_type: Optional[str] = "xgboost"


class PredictionUpdate(BaseModel):
    actual_value: float


class ModelMetricsResponse(BaseModel):
    metrics: List[dict]
    predictions: List[dict]


class OperationalMetricsResponse(BaseModel):
    metrics: List[dict]
