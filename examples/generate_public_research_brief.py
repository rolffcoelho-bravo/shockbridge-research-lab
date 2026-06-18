from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "examples" / "public_research_snapshot_v4_3.csv"
REPORT = ROOT / "reports" / "public_research_brief.md"

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

CITATION = "Pereira, R. (2026). ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research [Public research evidence repository]. GitHub. https://github.com/rolffcoelho-bravo/shockbridge-research-lab"


def clean(value):
    text = "" if value is None else str(value)
    for term in FORBIDDEN_TERMS:
        text = text.replace(term, "[non-public reference removed]")
    return text.replace("\n", " ").strip()


def read_snapshot():
    if not SNAPSHOT.exists():
        return [], []

    with SNAPSHOT.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        columns = [clean(c) for c in (reader.fieldnames or [])]
        rows = []
        for row in reader:
            rows.append({clean(k): clean(v) for k, v in row.items()})
        return columns, rows


def markdown_table(columns, rows, max_rows=10):
    if not columns or not rows:
        return "_No public snapshot rows were available for this demo._"

    visible_columns = columns[:6]
    visible_rows = rows[:max_rows]

    lines = []
    lines.append("| " + " | ".join(visible_columns) + " |")
    lines.append("| " + " | ".join(["---"] * len(visible_columns)) + " |")

    for row in visible_rows:
        lines.append("| " + " | ".join(clean(row.get(col, "")) for col in visible_columns) + " |")

    return "\n".join(lines)


def build_public_research_brief():
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    columns, rows = read_snapshot()
    column_list = ", ".join(columns) if columns else "No public snapshot columns found."
    preview = markdown_table(columns, rows)

    report = f"""# ShockBridge Public Research Brief

## Purpose

This public brief is generated from the sanitized ShockBridge Research Lab evidence repository. It demonstrates how the public layer organizes macro-financial shock transmission research without disclosing non-public calibration details, proprietary diagnostics, internal decision rules, or protected research files.

The goal is not to publish a trading signal. The goal is to show research structure, validation discipline, and public-facing analytical logic.

## Public demo output

Running the public pipeline generates this file:

reports/public_research_brief.md

## Research question

How can macro-financial stress move across markets before it becomes obvious in headline data?

ShockBridge Research Lab frames this question through a transmission-chain lens:

shock origin -> transmission channels -> regime diagnostics -> validation discipline -> public evidence layer

## Public framework

The public repository documents four visible layers:

1. Research architecture for cross-market shock transmission.
2. Data-source philosophy for macro-financial research.
3. Validation discipline, including time-aware testing and leakage control.
4. Public/private boundary rules that separate visible evidence from protected methodology.

## Public snapshot summary

Snapshot file used:

examples/public_research_snapshot_v4_3.csv

Detected public columns:

{column_list}

Detected public rows: {len(rows)}

### Snapshot preview

{preview}

## Interpretation discipline

The public repository is designed to show how a research desk can separate market movement, research evidence, and actionable decision logic.

This distinction matters because professional macro-financial work should not jump directly from a market move to a conclusion. A serious framework asks whether stress is isolated, transmitted, confirmed, persistent, or regime-relevant.

## What remains non-public

The public repository intentionally does not disclose non-public calibration details, protected diagnostic rules, internal scoring logic, research desk action policy, private validation files, or raw protected data.

## Professional use

This repository can be used as a public evidence layer for research applications, macro-finance discussions, quantitative finance positioning, risk and volatility research conversations, consulting-platform credibility, and portfolio or systemic-risk interviews.

It demonstrates that the author can structure a research project with documentation, validation awareness, citation discipline, and a clear public/private separation.

## Citation and attribution

If you use, reference, quote, adapt, or build from this public research evidence layer, please cite:

{CITATION}

Author: Rodolfo Pereira  
Website: www.shockbridgepulse.com  
Email: rolffcoelho@hotmail.com  

© 2026 Rodolfo P. Free to read and use with attribution. Please cite the author and repository when referencing this work.
"""

    REPORT.write_text(report, encoding="utf-8")
    return REPORT


if __name__ == "__main__":
    output = build_public_research_brief()
    print(f"Generated public research brief: {output}")
