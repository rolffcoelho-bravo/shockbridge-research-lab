"""Validation and backtesting tests."""

import pandas as pd

from shockbridge_lab.backtesting.overlay import (
    compute_strategy_returns,
    simple_regime_overlay_signal,
)
from shockbridge_lab.validation.time_split import chronological_split


def test_chronological_split() -> None:
    """Chronological split should preserve order and sizes."""
    X = pd.DataFrame({"x": range(10)})
    y = pd.Series(range(10))

    X_train, X_test, y_train, y_test = chronological_split(X, y, train_fraction=0.7)

    assert len(X_train) == 7
    assert len(X_test) == 3
    assert y_train.iloc[-1] == 6
    assert y_test.iloc[0] == 7


def test_simple_regime_overlay_signal() -> None:
    """Regime overlay should map regimes into exposure values."""
    regimes = pd.Series(["low", "medium", "high", "unknown"])
    exposure = simple_regime_overlay_signal(regimes)

    assert exposure.iloc[0] == 1.0
    assert exposure.iloc[1] == 0.7
    assert exposure.iloc[2] == 0.3
    assert exposure.iloc[3] == 0.5


def test_compute_strategy_returns() -> None:
    """Strategy returns should align returns and lagged exposure."""
    returns = pd.Series([0.01, 0.02, -0.01, 0.03])
    exposure = pd.Series([1.0, 0.7, 0.3, 1.0])

    strategy_returns = compute_strategy_returns(returns, exposure)

    assert len(strategy_returns) == 4
