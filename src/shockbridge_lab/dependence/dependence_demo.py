"""Public-safe dependence mapping utilities."""

import pandas as pd


def rolling_correlation(x: pd.Series, y: pd.Series, window: int = 60) -> pd.Series:
    """Compute rolling correlation as a simple dependence demonstration."""
    if window <= 1:
        raise ValueError("Window must be greater than 1.")

    aligned = pd.concat([x, y], axis=1).dropna()

    if aligned.shape[1] != 2:
        raise ValueError("Expected two aligned series.")

    return aligned.iloc[:, 0].rolling(window=window).corr(aligned.iloc[:, 1])
