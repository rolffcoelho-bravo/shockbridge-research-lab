from pathlib import Path
import subprocess
import sys
import os

ROOT = Path(__file__).resolve().parents[1]

OUTPUTS = [
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

def verify_outputs() -> None:
    for path in OUTPUTS:
        if not path.exists():
            raise SystemExit(f"Missing output: {path.relative_to(ROOT)}")

        if path.stat().st_size <= 0:
            raise SystemExit(f"Empty output: {path.relative_to(ROOT)}")

        print(f"OK: {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")

def main() -> None:
    open_outputs = "--open" in sys.argv

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

    print("ShockBridge public demo complete.")
    verify_outputs()

    if open_outputs:
        print("Opening generated public outputs...")
        for output in OUTPUTS:
            print(f"Opening: {output.relative_to(ROOT)}")
            open_file(output)

if __name__ == "__main__":
    main()
