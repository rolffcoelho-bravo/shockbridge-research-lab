import pandas as pd


def classify_volatility_regime(volatility: pd.Series) -> pd.Series:
    """Classify volatility into simple public-safe regimes."""
    if volatility.empty:
        raise ValueError("Volatility series is empty.")

    low_threshold = volatility.quantile(0.33)
    high_threshold = volatility.quantile(0.66)

    def label(value: float) -> str:
        if value <= low_threshold:
            return "low"
        if value >= high_threshold:
            return "high"
        return "medium"

    return volatility.apply(label)
