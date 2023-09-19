from sklearn.metrics import mean_squared_error, mean_absolute_error


def calculate_rmse(true_values: list, predicted_values: list) -> float:
    """Calculate the Root Mean Squared Error."""
    return mean_squared_error(true_values, predicted_values, squared=False)


def calculate_mae(true_values: list, predicted_values: list) -> float:
    """Calculate the Mean Absolute Error."""
    return mean_absolute_error(true_values, predicted_values)
