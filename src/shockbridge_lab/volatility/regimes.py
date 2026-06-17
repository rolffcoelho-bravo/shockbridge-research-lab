"""Public-safe volatility regime classification."""

import pandas as pd


def classify_volatility_regime(volatility: pd.Series) -> pd.Series:
    """Classify volatility into low, medium, and high regimes.

    This is a transparent public demonstration, not proprietary ShockBridge scoring.
    """
    clean_volatility = volatility.dropna()

    if clean_volatility.empty:
        raise ValueError("Volatility series is empty after dropping missing values.")

    low_threshold = clean_volatility.quantile(0.33)
    high_threshold = clean_volatility.quantile(0.66)

    def label(value: float) -> str:
        if value <= low_threshold:
            return "low"
        if value >= high_threshold:
            return "high"
        return "medium"

    return clean_volatility.apply(label)
