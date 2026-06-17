import numpy as np
import pandas as pd

from shockbridge_lab.features.market_features import compute_returns, rolling_volatility
from shockbridge_lab.volatility.regimes import classify_volatility_regime
from shockbridge_lab.backtesting.overlay import simple_regime_overlay_signal, compute_strategy_returns
from shockbridge_lab.reporting.report_writer import write_text_report


def main() -> None:
    np.random.seed(42)

    dates = pd.date_range("2020-01-01", periods=500, freq="B")
    prices = pd.Series(100 * (1 + np.random.normal(0.0003, 0.01, size=len(dates))).cumprod(), index=dates)

    returns = compute_returns(prices)
    volatility = rolling_volatility(returns, window=20)
    regimes = classify_volatility_regime(volatility.dropna())
    exposure = simple_regime_overlay_signal(regimes)

    strategy_returns = compute_strategy_returns(returns, exposure)
    total_return = strategy_returns.dropna().add(1).prod() - 1

    body = f'''
This public-safe example demonstrates the structure of a research pipeline.

Steps:
1. Generate demonstration price data
2. Compute returns
3. Estimate rolling volatility
4. Classify volatility regimes
5. Build a simple regime overlay
6. Compute illustrative strategy returns

Illustrative total return: {total_return:.4f}

Important: this is a public-safe demonstration and not the private ShockBridge Pulse methodology.
'''

    write_text_report(
        output_path="reports/example_research_report.md",
        title="ShockBridge Research Lab - Public Demo Report",
        body=body,
    )

    print("Pipeline completed. Report written to reports/example_research_report.md")


if __name__ == "__main__":
    main()
