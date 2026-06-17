import pandas as pd


def chronological_split(
    X: pd.DataFrame,
    y: pd.Series,
    train_fraction: float = 0.7,
):
    """Split data chronologically for time-series validation."""
    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1.")

    split_index = int(len(X) * train_fraction)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    return X_train, X_test, y_train, y_test
