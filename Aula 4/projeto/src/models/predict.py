import numpy as np
import xgboost as xgb


def predict_baseline(data: dict, model: float) -> float:
    """Make a prediction using the baseline model."""
    return model


def predict_xgboost(data: dict, model: xgb.XGBRegressor) -> float:
    """Make a prediction using the XGBoost model."""
    ASK = data["ASK"]
    ATK = data["ATK"]
    COMBUSTIVEL_LITROS = data["COMBUSTIVEL_LITROS"]

    pred = model.predict(np.array([[ASK, ATK, COMBUSTIVEL_LITROS]]))
    return float(pred[0])
