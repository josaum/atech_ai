# src/utils/model_utils.py

import os
import json
import xgboost as xgb

MODEL_DIR = "model_artifacts"
XGBOOST_MODEL_PATH = os.path.join(MODEL_DIR, "xgboost_model.json")
BASELINE_MODEL_PATH = os.path.join(MODEL_DIR, "baseline_model.json")


def save_xgboost_model(model: xgb.XGBRegressor):
    """Save the XGBoost model to a file."""
    model.save_model(XGBOOST_MODEL_PATH)


def load_xgboost_model() -> xgb.XGBRegressor:
    """Load the XGBoost model from a file."""
    model = xgb.XGBRegressor()
    model.load_model(XGBOOST_MODEL_PATH)
    return model


def save_baseline_model(value: float):
    """Save the baseline model value to a file."""
    with open(BASELINE_MODEL_PATH, "w") as f:
        json.dump({"baseline_value": value}, f)


def load_baseline_model() -> float:
    """Load the baseline model value from a file."""
    with open(BASELINE_MODEL_PATH, "r") as f:
        data = json.load(f)
    return data["baseline_value"]
