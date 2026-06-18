import argparse
import os
import sys

from generate_public_research_brief import build_public_research_brief
from generate_research_desk_pdf import build_research_desk_pdf


def open_file(path):
    if sys.platform.startswith("win"):
        os.startfile(str(path))
    elif sys.platform == "darwin":
        import subprocess
        subprocess.run(["open", str(path)], check=False)
    else:
        import subprocess
        subprocess.run(["xdg-open", str(path)], check=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the ShockBridge public demo pipeline.")
    parser.add_argument("--open", action="store_true", help="Open the generated PDF at the end.")
    args = parser.parse_args()

    md_output = build_public_research_brief()
    pdf_output = build_research_desk_pdf()

    print("ShockBridge public demo complete.")
    print(f"Generated Markdown brief: {md_output}")
    print(f"Generated one-page research desk PDF: {pdf_output}")

    if args.open:
        print("Opening generated PDF...")
        open_file(pdf_output)
