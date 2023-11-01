from typing import List, Dict, Optional
from pydantic import BaseModel


class InferencePayload(BaseModel):
    # {
    #     "ASK": 2397890.0,
    #     "ATK": 277088.0,
    #     "COMBUSTIVEL_LITROS": 85952.0
    # }
    ASK: float
    ATK: float
    COMBUSTIVEL_LITROS: float


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
