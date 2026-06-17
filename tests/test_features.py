"""Feature engineering tests."""

import pandas as pd

from shockbridge_lab.features.market_features import compute_returns, rolling_volatility
from shockbridge_lab.volatility.regimes import classify_volatility_regime


def test_compute_returns() -> None:
    """Returns should be calculated and should drop the initial missing value."""
    prices = pd.Series([100.0, 101.0, 102.0, 100.0])
    returns = compute_returns(prices)

    assert len(returns) == 3
    assert returns.isna().sum() == 0


def test_rolling_volatility() -> None:
    """Rolling volatility should return a series with the same index length."""
    returns = pd.Series([0.01, -0.02, 0.03, 0.01, -0.01])
    volatility = rolling_volatility(returns, window=2)

    assert len(volatility) == len(returns)


def test_classify_volatility_regime() -> None:
    """Volatility regime classifier should return valid labels."""
    volatility = pd.Series([0.01, 0.02, 0.03, 0.04, 0.05])
    regimes = classify_volatility_regime(volatility)

    assert set(regimes.unique()).issubset({"low", "medium", "high"})
