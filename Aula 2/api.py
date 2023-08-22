from fastapi import FastAPI, HTTPException, Depends
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
from typing import List, Dict, Optional

app = FastAPI()

# Variáveis globais para armazenar os modelos
baseline_model = None
xgb_model = None


# Função para calcular o valor médio do baseline
def train_baseline(df):
    return df.mean()


def train_xgb_model(df):
    X = df[["ASK", "ATK", "COMBUSTIVEL_LITROS", "PASSAGEIROS_PAGOS"]].dropna()
    y = X["PASSAGEIROS_PAGOS"]
    X = X.drop("PASSAGEIROS_PAGOS", axis=1)

    model = xgb.XGBRegressor(
        max_depth=5,
        n_estimators=100,
        learning_rate=0.1,
        objective="reg:squarederror",
        alpha=0.5,
    )
    model.fit(X, y)

    return model


@app.post("/train")
def train_models(data: List[Dict]):
    global baseline_model, xgb_model
    df = pd.DataFrame(data)

    baseline_model = train_baseline(df["PASSAGEIROS_PAGOS"])
    xgb_model = train_xgb_model(df)

    return {"message": "Models trained successfully"}


@app.post("/predict")
def predict_model(data: dict, model_type: Optional[str] = "xgboost"):
    ASK = data["ASK"]
    ATK = data["ATK"]
    COMBUSTIVEL_LITROS = data["COMBUSTIVEL_LITROS"]

    if model_type == "baseline":
        if baseline_model is None:
            raise HTTPException(
                status_code=400, detail="Baseline model has not been trained"
            )
        return {"prediction": float(baseline_model)}
    elif model_type == "xgboost":
        if xgb_model is None:
            raise HTTPException(
                status_code=400, detail="XGBoost model has not been trained"
            )
        pred = xgb_model.predict(np.array([[ASK, ATK, COMBUSTIVEL_LITROS]]))
        return {"prediction": float(pred[0])}
    else:
        raise HTTPException(status_code=400, detail="Model type not supported")
