from pathlib import Path
import subprocess
import sys
import os

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_OUTPUTS = [
    ROOT / "figures" / "public_cross_asset_stress_breadth.png",
    ROOT / "reports" / "public_research_brief.md",
    ROOT / "reports" / "ShockBridge_Public_Cross_Asset_Stress_Breadth_Desk_Note.pdf",
]

def open_file(path: Path) -> None:
    if sys.platform.startswith("win"):
        os.startfile(str(path))
    elif sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    else:
        subprocess.run(["xdg-open", str(path)], check=False)

def check_required_outputs() -> None:
    missing = []
    empty = []

    for path in REQUIRED_OUTPUTS:
        if not path.exists():
            missing.append(path)
        elif path.stat().st_size <= 0:
            empty.append(path)

    if missing or empty:
        lines = []
        if missing:
            lines.append("Missing outputs:")
            lines.extend(f"  - {p.relative_to(ROOT)}" for p in missing)
        if empty:
            lines.append("Empty outputs:")
            lines.extend(f"  - {p.relative_to(ROOT)}" for p in empty)
        raise SystemExit("\n".join(lines))

    print("ShockBridge public demo complete.")
    print(f"Generated README chart: {REQUIRED_OUTPUTS[0]}")
    print(f"Generated Markdown brief: {REQUIRED_OUTPUTS[1]}")
    print(f"Generated real-data one-page PDF: {REQUIRED_OUTPUTS[2]}")

def main() -> None:
    open_pdf = "--open" in sys.argv

    builder = ROOT / "examples" / "build_real_data_desk_page.py"

    if not builder.exists():
        raise SystemExit(f"Missing builder script: {builder}")

    result = subprocess.run(
        [sys.executable, str(builder)],
        cwd=str(ROOT),
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(result.returncode)

    check_required_outputs()

    if open_pdf:
        print("Opening generated PDF...")
        open_file(REQUIRED_OUTPUTS[2])

if __name__ == "__main__":
    main()
