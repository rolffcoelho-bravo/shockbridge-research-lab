import pandas as pd


def compute_returns(price_series: pd.Series) -> pd.Series:
    """Compute simple percentage returns from a price series."""
    if price_series.empty:
        raise ValueError("Price series is empty.")

    returns = price_series.pct_change()
    return returns.dropna()


def rolling_volatility(returns: pd.Series, window: int = 20) -> pd.Series:
    """Compute rolling volatility from returns."""
    if window <= 1:
        raise ValueError("Window must be greater than 1.")

    return returns.rolling(window=window).std()
