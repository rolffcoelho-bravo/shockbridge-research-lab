import pandas as pd


def simple_signal_energy(series: pd.Series, window: int = 20) -> pd.Series:
    """Compute a simplified signal-energy proxy.

    This is a public-safe demonstration and not a proprietary wavelet method.
    """
    if window <= 1:
        raise ValueError("Window must be greater than 1.")

    return series.pow(2).rolling(window=window).mean()
