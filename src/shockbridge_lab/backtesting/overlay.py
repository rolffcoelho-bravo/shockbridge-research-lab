"""Backtesting utilities for public-safe regime overlay examples."""

import pandas as pd


def simple_regime_overlay_signal(regime: pd.Series) -> pd.Series:
    """Create a simple exposure signal from volatility regimes."""
    mapping = {
        "low": 1.0,
        "medium": 0.7,
        "high": 0.3,
    }

    return regime.map(mapping).fillna(0.5)


def compute_strategy_returns(asset_returns: pd.Series, exposure: pd.Series) -> pd.Series:
    """Compute simple strategy returns using lagged exposure."""
    aligned = pd.concat([asset_returns, exposure], axis=1).dropna()
    aligned.columns = ["returns", "exposure"]

    return aligned["returns"] * aligned["exposure"].shift(1)
