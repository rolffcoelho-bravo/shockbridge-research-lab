from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_TERMS = [
    "METHODOLOGY_LOCK",
    "PRIVATE_CODE_AUDIT",
    "macro_confirmed_action_policy",
    "HEDGE_REVIEW",
    "official_macro_and_gold_anchor",
    "LBMA_GOLD_AM_LOCAL",
    "ml_walk_forward",
    "mcca_block_contribution",
    "FRED_API_KEY",
    "NASDAQ_DATA_LINK_API_KEY",
    "1b9e10b0",
]


def test_public_pipeline_generates_public_research_brief():
    result = subprocess.run(
        [sys.executable, "examples/run_full_pipeline.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    report = ROOT / "reports" / "public_research_brief.md"
    assert report.exists()

    text = report.read_text(encoding="utf-8")
    assert "ShockBridge Public Research Brief" in text
    assert "Public demo output" in text
    assert "Citation and attribution" in text

    for term in FORBIDDEN_TERMS:
        assert term not in text
