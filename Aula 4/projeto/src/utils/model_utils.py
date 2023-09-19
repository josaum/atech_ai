import os
import xgboost as xgb

MODEL_DIR = "model_artifacts"
XGBOOST_MODEL_PATH = os.path.join(MODEL_DIR, "xgboost_model.json")


def save_xgboost_model(model: xgb.XGBRegressor):
    """Save the XGBoost model to a file."""
    model.save_model(XGBOOST_MODEL_PATH)


def load_xgboost_model() -> xgb.XGBRegressor:
    """Load the XGBoost model from a file."""
    model = xgb.XGBRegressor()
    model.load_model(XGBOOST_MODEL_PATH)
    return model
