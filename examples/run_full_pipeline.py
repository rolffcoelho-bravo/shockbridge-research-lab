"""Run the public-safe ShockBridge Research Lab demo pipeline."""

import numpy as np
import pandas as pd

from shockbridge_lab.backtesting.overlay import (
    compute_strategy_returns,
    simple_regime_overlay_signal,
)
from shockbridge_lab.features.market_features import compute_returns, rolling_volatility
from shockbridge_lab.reporting.report_writer import write_text_report
from shockbridge_lab.volatility.regimes import classify_volatility_regime


def main() -> None:
    """Run a complete public-safe research pipeline."""
    np.random.seed(42)

    dates = pd.date_range("2020-01-01", periods=500, freq="B")
    shocks = np.random.normal(0.0003, 0.01, size=len(dates))
    prices = pd.Series(
        100 * (1 + shocks).cumprod(),
        index=dates,
        name="demo_price",
    )

    returns = compute_returns(prices)
    volatility = rolling_volatility(returns, window=20)
    regimes = classify_volatility_regime(volatility)
    exposure = simple_regime_overlay_signal(regimes)

    strategy_returns = compute_strategy_returns(returns, exposure)
    total_return = strategy_returns.dropna().add(1).prod() - 1

    body = f"""
This public-safe example demonstrates the structure of a macro-financial research pipeline.

Pipeline steps:

1. Generate demonstration market data.
2. Compute returns.
3. Estimate rolling volatility.
4. Classify volatility regimes.
5. Build a simple regime overlay.
6. Compute illustrative strategy returns.
7. Write a reproducible research report.

Illustrative total return: {total_return:.4f}

Important: this is a public evidence demonstration. It is not the private ShockBridge Pulse methodology.
"""

    write_text_report(
        output_path="reports/example_research_report.md",
        title="ShockBridge Research Lab - Public Demo Report",
        body=body,
    )

    print("Pipeline completed.")
    print("Report written to reports/example_research_report.md")


if __name__ == "__main__":
    main()
