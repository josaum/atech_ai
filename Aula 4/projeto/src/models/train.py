import numpy as np
import pandas as pd
import xgboost as xgb


def train_baseline_model(data: pd.DataFrame) -> float:
    """Train a simple baseline model."""
    # dropna and also not None
    return np.mean(pd.to_numeric(data["PASSAGEIROS_PAGOS"]).sort_values().dropna())


def train_xgboost_model(data: pd.DataFrame) -> xgb.XGBRegressor:
    """Train an XGBoost regression model."""
    for column in ["ASK", "ATK", "COMBUSTIVEL_LITROS", "PASSAGEIROS_PAGOS"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    X = data[["ASK", "ATK", "COMBUSTIVEL_LITROS", "PASSAGEIROS_PAGOS"]].dropna()
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
