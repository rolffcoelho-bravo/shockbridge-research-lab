import argparse
import os
import sys
import shutil
from pathlib import Path

from generate_public_research_brief import build_public_research_brief
from build_real_data_desk_page import build_artifact

ROOT = Path(__file__).resolve().parents[1]
PIPELINE_CHART = ROOT / "reports" / "_real_public_stress_breadth_chart.png"
README_CHART = ROOT / "figures" / "public_cross_asset_stress_breadth.png"


def open_file(path):
    if sys.platform.startswith("win"):
        os.startfile(str(path))
    elif sys.platform == "darwin":
        import subprocess
        subprocess.run(["open", str(path)], check=False)
    else:
        import subprocess
        subprocess.run(["xdg-open", str(path)], check=False)


def sync_readme_chart():
    if not PIPELINE_CHART.exists():
        raise FileNotFoundError(f"Pipeline chart was not generated: {PIPELINE_CHART}")

    README_CHART.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PIPELINE_CHART, README_CHART)
    return README_CHART


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the ShockBridge public real-data demo pipeline.")
    parser.add_argument("--open", action="store_true", help="Open the generated PDF at the end.")
    parser.add_argument("--refresh", action="store_true", help="Refresh real public market data.")
    args = parser.parse_args()

    md_output = build_public_research_brief()
    pdf_output = build_artifact(refresh=args.refresh)
    chart_output = sync_readme_chart()

    print("ShockBridge public demo complete.")
    print(f"Generated Markdown brief: {md_output}")
    print(f"Generated README chart: {chart_output}")
    print(f"Generated real-data one-page PDF: {pdf_output}")

    if args.open:
        print("Opening generated PDF...")
        open_file(pdf_output)
