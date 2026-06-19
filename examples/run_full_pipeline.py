from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

PNG = ROOT / "figures" / "public_cross_asset_stress_breadth.png"
MD = ROOT / "reports" / "public_research_brief.md"
PDF = ROOT / "reports" / "ShockBridge_Public_Cross_Asset_Stress_Breadth_Desk_Note.pdf"

OUTPUTS = [PNG, MD, PDF]


def verify_outputs() -> None:
    for path in OUTPUTS:
        if not path.exists():
            raise SystemExit(f"Missing output: {path.relative_to(ROOT)}")

        if path.stat().st_size <= 0:
            raise SystemExit(f"Empty output: {path.relative_to(ROOT)}")

        print(f"OK: {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


def invoke_item(path: Path) -> None:
    subprocess.Popen(
        [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"Invoke-Item -LiteralPath '{str(path)}'",
        ],
        cwd=str(ROOT),
    )


def main() -> None:
    open_outputs = "--open" in sys.argv

    builder = ROOT / "examples" / "build_real_data_desk_page.py"

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
        invoke_item(PNG)
        invoke_item(MD)
        invoke_item(PDF)


if __name__ == "__main__":
    main()
