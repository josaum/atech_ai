from fastapi import APIRouter, HTTPException
import datetime
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
import logging

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
    logging.info("Models trained and saved successfully.")
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
    # Salvar a previsão no banco de dados
    try:
        current_timestamp = (
            datetime.datetime.now()
        )  # você pode precisar importar datetime
        db.insert_prediction(
            timestamp=current_timestamp,
            model_type=prediction_data.model_type,
            input_data=str(prediction_data.data),
            predicted_value=prediction,
        )
        logging.info(f"Prediction saved for model {prediction_data.model_type}.")
    except Exception as e:
        logging.error(f"Error saving prediction: {e}")
        # Caso haja algum erro ao salvar no banco de dados, você pode lidar com ele aqui
        raise HTTPException(
            status_code=500, detail=f"Error saving prediction: {str(e)}"
        )

    return {"prediction": prediction}


@router.put("/prediction/{prediction_id}")
def update_prediction(prediction_id: int, update_data: PredictionUpdate):
    try:
        db.update_actual_value_by_id(prediction_id, update_data.actual_value)
        logging.info(f"Prediction with ID {prediction_id} updated successfully.")
        return {"message": f"Prediction with ID {prediction_id} updated successfully"}
    except Exception as e:
        logging.error(f"Error updating prediction with ID {prediction_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metrics/model")
def get_model_metrics() -> ModelMetricsResponse:
    try:
        metrics = db.fetch_ml_metrics()
        predictions = db.fetch_predictions()
        logging.info("Model metrics fetched successfully.")
        return ModelMetricsResponse(metrics=metrics, predictions=predictions)
    except Exception as e:
        logging.error(f"Error fetching model metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/operational")
def get_operational_metrics() -> OperationalMetricsResponse:
    try:
        metrics = db.fetch_operational_metrics()
        logging.info("Operational metrics fetched successfully.")
        return OperationalMetricsResponse(metrics=metrics)
    except Exception as e:
        logging.error(f"Error fetching operational metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
