from fastapi import APIRouter, HTTPException
import pandas as pd
from typing import List, Dict, Optional

# Importando funções dos scripts criados
from src.models import train, predict
from src.utils import model_utils
from src.monitoring import monitor
import duckdb

router = APIRouter()

baseline_model = None
xgb_model = None


@router.post("/train")
def train_models(data: List[Dict]):
    global baseline_model, xgb_model
    df = pd.DataFrame(data)

    # Treinando os modelos
    baseline_model = train.train_baseline_model(df)
    xgb_model = train.train_xgboost_model(df)

    # Salvando o modelo XGBoost
    model_utils.save_xgboost_model(xgb_model)

    return {"message": "Models trained successfully"}


@router.post("/predict")
def predict_model(data: dict, model_type: Optional[str] = "xgboost"):
    if model_type == "baseline":
        if baseline_model is None:
            raise HTTPException(
                status_code=400, detail="Baseline model has not been trained"
            )
        prediction = predict.predict_baseline(data, baseline_model)

    elif model_type == "xgboost":
        # Carregando o modelo XGBoost
        if xgb_model is None:
            xgb_model = model_utils.load_xgboost_model()

        prediction = predict.predict_xgboost(data, xgb_model)

    else:
        raise HTTPException(status_code=400, detail="Model type not supported")

    return {"prediction": prediction}


@router.get("/metrics/operational")
def get_operational_metrics():
    con = duckdb.connect(database=":memory:", read_only=True)
    results = con.execute("SELECT * FROM operational_metrics").fetchall()
    con.close()
    return {"data": results}


@router.get("/metrics/ml")
def get_ml_metrics():
    con = duckdb.connect(database=":memory:", read_only=True)
    results = con.execute("SELECT * FROM ml_metrics").fetchall()
    con.close()
    return {"data": results}
