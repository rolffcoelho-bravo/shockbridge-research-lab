from pathlib import Path
import argparse
import base64
import os
import shutil
import subprocess
import sys
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public" / "public_cross_asset_prices.csv"
REPORTS = ROOT / "reports"
CHART = REPORTS / "_real_public_stress_breadth_chart.png"
FIGURE = ROOT / "figures" / "public_cross_asset_stress_breadth.png"
HTML = REPORTS / "regime_question_one_page.html"
PDF = REPORTS / "ShockBridge_Public_Cross_Asset_Stress_Breadth_Desk_Note.pdf"

TICKERS = ["SPY", "QQQ", "TLT", "GLD", "USO", "UUP", "HYG"]

BROWSER_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def find_browser():
    for candidate in BROWSER_CANDIDATES:
        if Path(candidate).exists():
            return candidate

    for name in ["chrome", "chrome.exe", "msedge", "msedge.exe"]:
        found = shutil.which(name)
        if found:
            return found

    raise RuntimeError("No Chrome or Microsoft Edge executable found for PDF export.")


def download_real_public_data(refresh=False):
    DATA.parent.mkdir(parents=True, exist_ok=True)

    if DATA.exists() and not refresh:
        return DATA

    raw = yf.download(
        TICKERS,
        start="2023-01-01",
        auto_adjust=True,
        progress=False,
        group_by="column",
    )

    if raw.empty:
        raise RuntimeError("No public market data returned by yfinance. I will not fabricate data.")

    if isinstance(raw.columns, pd.MultiIndex):
        close = raw["Close"].copy()
    else:
        close = raw[["Close"]].copy()

    close = close.dropna(how="all")
    close.index.name = "date"
    close = close.reset_index()
    close.to_csv(DATA, index=False)

    return DATA


def load_prices():
    if not DATA.exists():
        raise FileNotFoundError("Real public market data not found. Run the pipeline with data download enabled.")

    df = pd.read_csv(DATA)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")

    numeric = [c for c in df.columns if c != "date"]

    for c in numeric:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(how="all", subset=numeric)

    if df.empty:
        raise ValueError("Public market data CSV exists but has no usable rows.")

    return df, numeric


def compute_stress(df, numeric):
    prices = df[numeric].copy()
    returns = prices.pct_change()

    realized_vol = returns.rolling(21).std()
    drawdown = prices / prices.rolling(63).max() - 1

    stress = pd.DataFrame(index=df.index)

    for c in numeric:
        vol_percentile = realized_vol[c].rank(pct=True)
        drawdown_percentile = (-drawdown[c]).rank(pct=True)
        stress[c] = 100 * ((0.55 * vol_percentile) + (0.45 * drawdown_percentile))

    stress = stress.dropna(how="all")

    breadth = pd.DataFrame({
        "date": df.loc[stress.index, "date"],
        "stress_breadth_75": (stress >= 75).mean(axis=1) * 100,
        "stress_breadth_60": (stress >= 60).mean(axis=1) * 100,
        "median_stress": stress.median(axis=1),
    }).dropna()

    if breadth.empty:
        raise ValueError("Not enough real observations to compute public stress breadth.")

    return stress, breadth


def build_chart(stress, breadth):
    REPORTS.mkdir(parents=True, exist_ok=True)

    bg = "#07111f"
    panel = "#0b1220"
    text = "#f8fafc"
    muted = "#94a3b8"
    gold = "#f5c76b"
    blue = "#38bdf8"
    red = "#ef4444"

    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    ax.plot(
        breadth["date"],
        breadth["stress_breadth_75"],
        color=gold,
        linewidth=2.8,
        label="% of assets above own 75th stress percentile",
    )

    ax.plot(
        breadth["date"],
        breadth["stress_breadth_60"],
        color=blue,
        linewidth=1.8,
        alpha=0.9,
        label="% of assets above own 60th stress percentile",
    )

    ax.plot(
        breadth["date"],
        breadth["median_stress"],
        color="#cbd5e1",
        linewidth=1.5,
        linestyle="--",
        alpha=0.9,
        label="Median cross-asset stress percentile",
    )

    ax.axhline(50, color=red, linewidth=1.0, linestyle=":", alpha=0.9)
    ax.text(
        breadth["date"].iloc[0],
        52,
        "50% breadth line",
        fontsize=8,
        color="#fecaca",
    )

    latest_75 = float(breadth["stress_breadth_75"].iloc[-1])
    latest_median = float(breadth["median_stress"].iloc[-1])

    ax.text(
        0.012,
        0.92,
        f"Latest 75th-percentile breadth: {latest_75:.1f}% | Median stress percentile: {latest_median:.1f}",
        transform=ax.transAxes,
        fontsize=8.5,
        color=text,
        bbox=dict(facecolor=panel, edgecolor="#334155", boxstyle="round,pad=0.35"),
    )

    ax.set_title(
        "Real public cross-asset stress breadth",
        loc="left",
        fontsize=14,
        fontweight="bold",
        color=text,
        pad=10,
    )

    ax.set_ylabel("Stress breadth / percentile position", color=text, fontsize=9)
    ax.set_ylim(0, 105)

    ax.grid(True, axis="y", alpha=0.20, color="#334155")
    ax.grid(True, axis="x", alpha=0.10, color="#334155")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#475569")
    ax.spines["bottom"].set_color("#475569")

    ax.tick_params(axis="both", labelsize=8, colors="#cbd5e1")

    fig.tight_layout()
    fig.savefig(CHART, dpi=240, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)

    FIGURE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CHART, FIGURE)

    return CHART


def build_bullets(stress, breadth):
    latest = breadth.iloc[-1]
    previous = breadth.iloc[max(0, len(breadth) - 22)]

    latest_75 = float(latest["stress_breadth_75"])
    latest_60 = float(latest["stress_breadth_60"])
    median = float(latest["median_stress"])
    change = latest_75 - float(previous["stress_breadth_75"])

    latest_components = stress.iloc[-1].sort_values(ascending=False)
    leader = latest_components.index[0]
    second = latest_components.index[1]
    third = latest_components.index[2]
    leader_value = float(latest_components.iloc[0])
    concentration_gap = leader_value - median

    if latest_75 >= 50:
        breadth_read = "broad enough to be treated as a public cross-asset transmission watch."
    elif latest_75 >= 25:
        breadth_read = "partially broadening, but not yet a broad public regime signal."
    else:
        breadth_read = "still narrow, so the public evidence does not yet support a broad regime call."

    if change > 10:
        direction_read = "accelerating"
    elif change < -10:
        direction_read = "cooling"
    else:
        direction_read = "stable"

    if concentration_gap > 30:
        concentration_read = "stress is still concentrated in one leading sleeve."
    else:
        concentration_read = "stress is becoming more evenly distributed across the visible sleeves."

    return [
        f"Public stress breadth is {latest_75:.1f}%: {breadth_read}",
        f"One-month direction is {direction_read}: the 75th-percentile breadth changed {change:.1f} percentage points.",
        f"Depth is meaningful but not absolute: median cross-asset stress is at the {median:.1f}th percentile and {latest_60:.1f}% of assets are above their 60th stress percentile.",
        f"Leadership is visible: {leader}, {second}, and {third} are the strongest current public stress components; {leader} sits at the {leader_value:.1f}th percentile.",
        f"Concentration check: the leader is {concentration_gap:.1f} percentile points above the median, meaning {concentration_read}",
        "Research-desk implication: the question is not whether one market moved, but whether public stress is broadening enough to justify a regime-transmission watch.",
    ]


def chart_as_base64(path):
    payload = path.read_bytes()
    return base64.b64encode(payload).decode("ascii")


def build_html(chart_path, bullets, df, numeric):
    chart_b64 = chart_as_base64(chart_path)
    generated = datetime.utcnow().strftime("%Y-%m-%d UTC")

    sample_start = df["date"].min().date()
    sample_end = df["date"].max().date()

    bullet_html = "\n".join(
        f"<li>{b}</li>" for b in bullets
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ShockBridge Real-Data Research Desk Page</title>
<style>
@page {{
    size: A4 portrait;
    margin: 0;
}}
html, body {{
    margin: 0;
    padding: 0;
    width: 210mm;
    height: 297mm;
    background: #07111f;
    font-family: Arial, Helvetica, sans-serif;
}}
.page {{
    width: 210mm;
    height: 297mm;
    box-sizing: border-box;
    padding: 13mm 14mm 11mm 14mm;
    background:
        radial-gradient(circle at 18% 8%, rgba(56,189,248,0.15), transparent 26%),
        linear-gradient(135deg, #07111f 0%, #0b1220 55%, #111827 100%);
    color: #f8fafc;
    overflow: hidden;
}}
.border {{
    border: 1px solid #d6a14a;
    height: 100%;
    box-sizing: border-box;
    padding: 8mm 9mm 10mm 9mm;
    display: flex;
    flex-direction: column;
}}
.kicker {{
    display: flex;
    justify-content: space-between;
    font-size: 7.2pt;
    letter-spacing: 1.2px;
    color: #f5c76b;
    text-transform: uppercase;
    border-bottom: 1px solid #334155;
    padding-bottom: 4mm;
}}
h1 {{
    margin: 6mm 0 2mm 0;
    font-size: 20pt;
    line-height: 1.06;
    color: #fff7ed;
    font-weight: 800;
}}
.subtitle {{
    font-size: 8.7pt;
    color: #94a3b8;
    margin-bottom: 4mm;
}}
.meta {{
    display: flex;
    gap: 10mm;
    color: #f5c76b;
    font-size: 7.2pt;
    font-weight: 700;
    margin-bottom: 4mm;
}}
.chart-panel {{
    border: 1px solid #334155;
    background: rgba(11,18,32,0.82);
    padding: 3mm 4mm 3mm 4mm;
    border-radius: 4mm;
    margin-bottom: 4mm;
}}
.chart-panel img {{
    display: block;
    width: 100%;
    height: 108mm;
    object-fit: contain;
}}

.chart-legend {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.8mm 7mm;
    margin-top: 2.2mm;
    padding-top: 2.2mm;
    border-top: 1px solid #334155;
    color: #cbd5e1;
    font-size: 7.2pt;
    line-height: 1.22;
}}
.legend-item {{
    display: flex;
    align-items: center;
    gap: 2mm;
}}
.legend-line {{
    width: 14mm;
    height: 0;
    border-top: 2px solid;
    display: inline-block;
}}
.legend-gold {{ border-color: #f5c76b; }}
.legend-blue {{ border-color: #38bdf8; }}
.legend-gray {{ border-color: #cbd5e1; border-top-style: dashed; }}
.legend-red {{ border-color: #ef4444; border-top-style: dotted; }}

.readout {{
    border: 1px solid #d6a14a;
    border-radius: 4mm;
    background: rgba(11,18,32,0.84);
    padding: 4.2mm 6mm 3.8mm 6mm;
    margin-top: 0;
    margin-bottom: 5mm;
    flex: 0 0 auto;
}}
.readout h2 {{
    color: #f5c76b;
    font-size: 13pt;
    margin: 0 0 3mm 0;
}}
.readout ul {{
    margin: 0;
    padding-left: 5mm;
}}
.readout li {{
    color: #f8fafc;
    font-size: 8.5pt;
    line-height: 1.35;
    margin-bottom: 2.15mm;
}}
.footer {{
    margin-top: 0;
    padding-top: 0;
    border-top: none;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 14mm;
    color: #94a3b8;
    flex: 0 0 auto;
}}

.footer-left,
.footer-right {{
    font-size: 6.9pt;
    line-height: 1.25;
    color: rgba(203,213,225,0.76);
}}

.footer-left {{
    max-width: 58%;
}}

.footer-right {{
    max-width: 34%;
    text-align: right;
}}

.footer .line1 {{
    color: rgba(248,250,252,0.88);
    font-weight: 600;
}}

.footer .line2 {{
    margin-top: 0.7mm;
    color: rgba(203,213,225,0.68);
}}
.footer-left,
.footer-right {{
    font-size: 7.4pt;
    line-height: 1.35;
    color: rgba(226,232,240,0.72);
}}
.footer-left {{
    max-width: 58%;
}}
.footer-right {{
    max-width: 34%;
    text-align: right;
}}
.footer .line1 {{
    color: rgba(248,250,252,0.88);
    font-weight: 600;
}}
.footer .line2 {{
    margin-top: 1mm;
    color: rgba(203,213,225,0.70);
}}
</style>
</head>
<body>
<div class="page">
<div class="border">

<div class="kicker">
    <div>ShockBridge Research Lab</div>
    <div>Public real-data desk page · Generated {generated}</div>
</div>

<h1>Is Public Cross-Asset Stress Broadening or Staying Isolated?</h1>
<div class="subtitle">
Real public market data only: SPY, QQQ, TLT, GLD, USO, UUP, HYG. No synthetic data, no private thresholds, no private action rules.
</div>

<div class="meta">
    <div>Rows: {len(df)}</div>
    <div>Assets: {len(numeric)}</div>
    <div>Sample: {sample_start} to {sample_end}</div>
</div>

<div class="chart-panel">
    <img src="data:image/png;base64,{chart_b64}" alt="Real public cross-asset stress breadth chart">

    <div class="chart-legend">
        <div class="legend-item"><span class="legend-line legend-gold"></span><span>% of assets above own 75th stress percentile</span></div>
        <div class="legend-item"><span class="legend-line legend-blue"></span><span>% of assets above own 60th stress percentile</span></div>
        <div class="legend-item"><span class="legend-line legend-gray"></span><span>Median cross-asset stress percentile</span></div>
        <div class="legend-item"><span class="legend-line legend-red"></span><span>50% breadth reference line</span></div>
    </div>
</div>

<div class="readout">
    <h2>Research-desk readout from real public data</h2>
    <ul>
        {bullet_html}
    </ul>
</div>

<div class="footer">
    <div class="footer-left">
        <div class="line1">Rodolfo P. | ShockBridge Research Lab</div>
        <div class="line2">www.shockbridgepulse.com | rolffcoelho@hotmail.com</div>
    </div>
    <div class="footer-right">
        <div class="line1">© 2026 Rodolfo P.</div>
        <div class="line2">Public research evidence repository</div>
    </div>
</div>

</div>
</div>
</body>
</html>
"""
    HTML.write_text(html, encoding="utf-8")
    return HTML


def export_pdf():
    browser = find_browser()

    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--print-to-pdf=" + str(PDF),
        str(HTML.resolve().as_uri()),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        raise RuntimeError(
            "PDF export failed.\n"
            f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        )

    if not PDF.exists() or PDF.stat().st_size < 1000:
        raise RuntimeError("PDF export failed or produced an empty file.")

    reader = PdfReader(str(PDF))
    if len(reader.pages) != 1:
        raise RuntimeError(f"Expected one PDF page, got {len(reader.pages)}")

    return PDF


def build_artifact(refresh=False):
    download_real_public_data(refresh=refresh)
    df, numeric = load_prices()
    stress, breadth = compute_stress(df, numeric)
    chart = build_chart(stress, breadth)
    bullets = build_bullets(stress, breadth)
    build_html(chart, bullets, df, numeric)
    return export_pdf()


def open_file(path):
    if sys.platform.startswith("win"):
        os.startfile(str(path))
    elif sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    else:
        subprocess.run(["xdg-open", str(path)], check=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Refresh real public market data.")
    parser.add_argument("--open", action="store_true", help="Open generated PDF.")
    args = parser.parse_args()

    output = build_artifact(refresh=args.refresh)
    print(f"Generated real-data one-page PDF: {output}")

    if args.open:
        open_file(output)
