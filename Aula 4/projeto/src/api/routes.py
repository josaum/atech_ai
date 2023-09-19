from fastapi import APIRouter, HTTPException
import pandas as pd
from src.models import train, predict
from src.utils import model_utils, db_manager
from .models import (
    PredictionData,
    PredictionUpdate,
    ModelMetricsResponse,
    OperationalMetricsResponse,
)
import os

router = APIRouter()
db = db_manager.DBManager()
PARQUET_PATH = os.path.join("data", "processed", "input_dataset.parquet")


@router.post("/train")
def train_models():
    df = pd.read_parquet(PARQUET_PATH)

    # Train the models
    baseline_value = train.train_baseline_model(df)
    xgb_model = train.train_xgboost_model(df)

    # Save the models
    model_utils.save_baseline_model(baseline_value)
    model_utils.save_xgboost_model(xgb_model)

    return {"message": "Models trained successfully"}


@router.post("/predict")
def predict_model(prediction_data: PredictionData):
    if prediction_data.model_type == "baseline":
        baseline_value = model_utils.load_baseline_model()
        prediction = predict.predict_baseline(prediction_data.data, baseline_value)
    elif prediction_data.model_type == "xgboost":
        xgb_model = model_utils.load_xgboost_model()
        prediction = predict.predict_xgboost(prediction_data.data, xgb_model)
    else:
        raise HTTPException(status_code=400, detail="Model type not supported")
    return {"prediction": prediction}


@router.put("/prediction/{prediction_id}")
def update_prediction(prediction_id: int, update_data: PredictionUpdate):
    try:
        db.update_actual_value_by_id(prediction_id, update_data.actual_value)
        return {"message": f"Prediction with ID {prediction_id} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metrics/model")
def get_model_metrics() -> ModelMetricsResponse:
    metrics = db.fetch_ml_metrics()
    predictions = db.fetch_predictions()
    return ModelMetricsResponse(metrics=metrics, predictions=predictions)


@router.get("/metrics/operational")
def get_operational_metrics() -> OperationalMetricsResponse:
    metrics = db.fetch_operational_metrics()
    return OperationalMetricsResponse(metrics=metrics)
