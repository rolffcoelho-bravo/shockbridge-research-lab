from pathlib import Path

def write(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")

write(".github/workflows/tests.yml", """
name: tests

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    env:
      PYTHONPATH: src

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt

      - name: Run tests
        run: |
          python -m pytest -q

      - name: Run demo pipeline
        run: |
          python examples/run_full_pipeline.py
""")

write("pyproject.toml", """
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "shockbridge-research-lab"
version = "0.1.0"
description = "Public evidence portfolio for macro-financial research engineering."
authors = [
    { name = "Rodolfo Pereira" }
]
requires-python = ">=3.10"
dependencies = [
    "pandas>=2.2.0",
    "numpy>=1.26.0",
    "scikit-learn>=1.4.0",
    "matplotlib>=3.8.0"
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.black]
line-length = 100
target-version = ["py310"]

[tool.mypy]
python_version = "3.10"
ignore_missing_imports = true
""")

write("src/shockbridge_lab/__init__.py", '''
"""ShockBridge Research Lab.

Public evidence portfolio for macro-financial research engineering.
"""

__version__ = "0.1.0"
''')

write("src/shockbridge_lab/features/market_features.py", '''
"""Market feature engineering utilities."""

import pandas as pd


def compute_returns(price_series: pd.Series) -> pd.Series:
    """Compute simple percentage returns from a price series."""
    if price_series.empty:
        raise ValueError("Price series is empty.")

    returns = price_series.pct_change()
    return returns.dropna()


def rolling_volatility(returns: pd.Series, window: int = 20) -> pd.Series:
    """Compute rolling volatility from returns."""
    if returns.empty:
        raise ValueError("Returns series is empty.")

    if window <= 1:
        raise ValueError("Window must be greater than 1.")

    return returns.rolling(window=window).std()
''')

write("src/shockbridge_lab/volatility/regimes.py", '''
"""Public-safe volatility regime classification."""

import pandas as pd


def classify_volatility_regime(volatility: pd.Series) -> pd.Series:
    """Classify volatility into low, medium, and high regimes."""
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
''')

write("src/shockbridge_lab/backtesting/overlay.py", '''
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
''')

write("src/shockbridge_lab/reporting/report_writer.py", '''
"""Report writing utilities."""

from pathlib import Path


def write_text_report(output_path: str | Path, title: str, body: str) -> Path:
    """Write a simple markdown report."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    content = f"# {title}\\n\\n{body}\\n"
    path.write_text(content, encoding="utf-8")

    return path
''')

write("examples/run_full_pipeline.py", '''
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
''')

write("tests/test_features.py", '''
"""Feature engineering tests."""

import pandas as pd

from shockbridge_lab.features.market_features import compute_returns, rolling_volatility
from shockbridge_lab.volatility.regimes import classify_volatility_regime


def test_compute_returns() -> None:
    prices = pd.Series([100.0, 101.0, 102.0, 100.0])
    returns = compute_returns(prices)

    assert len(returns) == 3
    assert returns.isna().sum() == 0


def test_rolling_volatility() -> None:
    returns = pd.Series([0.01, -0.02, 0.03, 0.01, -0.01])
    volatility = rolling_volatility(returns, window=2)

    assert len(volatility) == len(returns)


def test_classify_volatility_regime() -> None:
    volatility = pd.Series([0.01, 0.02, 0.03, 0.04, 0.05])
    regimes = classify_volatility_regime(volatility)

    assert set(regimes.unique()).issubset({"low", "medium", "high"})
''')

write("tests/test_validation_and_backtest.py", '''
"""Backtesting tests."""

import pandas as pd

from shockbridge_lab.backtesting.overlay import (
    compute_strategy_returns,
    simple_regime_overlay_signal,
)


def test_simple_regime_overlay_signal() -> None:
    regimes = pd.Series(["low", "medium", "high", "unknown"])
    exposure = simple_regime_overlay_signal(regimes)

    assert exposure.iloc[0] == 1.0
    assert exposure.iloc[1] == 0.7
    assert exposure.iloc[2] == 0.3
    assert exposure.iloc[3] == 0.5


def test_compute_strategy_returns() -> None:
    returns = pd.Series([0.01, 0.02, -0.01, 0.03])
    exposure = pd.Series([1.0, 0.7, 0.3, 1.0])

    strategy_returns = compute_strategy_returns(returns, exposure)

    assert len(strategy_returns) == 4
''')
