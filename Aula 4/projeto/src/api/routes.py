# src/api/routes.py

from fastapi import APIRouter, HTTPException
import pandas as pd
from typing import List, Dict, Optional
from src.models import train, predict
from src.utils import model_utils, db_manager

router = APIRouter()
db = db_manager.DBManager()


@router.post("/train")
def train_models(data: List[Dict]):
    df = pd.DataFrame(data)

    # Train the models
    baseline_value = train.train_baseline_model(df)
    xgb_model = train.train_xgboost_model(df)

    # Save the models
    model_utils.save_baseline_model(baseline_value)
    model_utils.save_xgboost_model(xgb_model)

    return {"message": "Models trained successfully"}


@router.post("/predict")
def predict_model(data: dict, model_type: Optional[str] = "xgboost"):
    if model_type == "baseline":
        baseline_value = model_utils.load_baseline_model()
        prediction = predict.predict_baseline(data, baseline_value)
    elif model_type == "xgboost":
        xgb_model = model_utils.load_xgboost_model()
        prediction = predict.predict_xgboost(data, xgb_model)
    else:
        raise HTTPException(status_code=400, detail="Model type not supported")
    return {"prediction": prediction}


@router.get("/metrics/model")
def get_model_metrics():
    metrics = db.fetch_ml_metrics()
    predictions = db.fetch_predictions()  # Define this method in DBManager
    return {"metrics": metrics, "predictions": predictions}
