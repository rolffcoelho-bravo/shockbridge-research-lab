"""Public-safe signal-processing demonstrations."""

import pandas as pd


def simple_signal_energy(series: pd.Series, window: int = 20) -> pd.Series:
    """Compute a simplified rolling signal-energy proxy.

    This is not a proprietary wavelet method.
    """
    if series.empty:
        raise ValueError("Input series is empty.")

    if window <= 1:
        raise ValueError("Window must be greater than 1.")

    return series.pow(2).rolling(window=window).mean()
