"""Repository structure tests."""

from pathlib import Path


def test_required_directories_exist() -> None:
    """Check that required evidence-lab directories exist."""
    required_dirs = [
        "docs",
        "data/raw",
        "data/processed",
        "src/shockbridge_lab",
        "src/shockbridge_lab/ingestion",
        "src/shockbridge_lab/features",
        "src/shockbridge_lab/volatility",
        "src/shockbridge_lab/dependence",
        "src/shockbridge_lab/signal_processing",
        "src/shockbridge_lab/ml",
        "src/shockbridge_lab/backtesting",
        "src/shockbridge_lab/validation",
        "src/shockbridge_lab/reporting",
        "tests",
        "examples",
        "reports",
    ]

    for folder in required_dirs:
        assert Path(folder).exists(), f"Missing required folder: {folder}"


def test_required_files_exist() -> None:
    """Check that required portfolio files exist."""
    required_files = [
        "README.md",
        "PORTFOLIO_MAP.md",
        "PUBLIC_EVIDENCE_BOUNDARY.md",
        "DATA_POLICY.md",
        "pyproject.toml",
        "requirements.txt",
        "Dockerfile",
    ]

    for file in required_files:
        assert Path(file).exists(), f"Missing required file: {file}"
