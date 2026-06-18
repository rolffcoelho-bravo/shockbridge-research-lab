from pathlib import Path
import subprocess
import sys
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def test_public_pipeline_generates_exactly_one_page_professional_pdf():
    result = subprocess.run(
        [sys.executable, "examples/run_full_pipeline.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    pdf = ROOT / "reports" / "ShockBridge_Public_Cross_Asset_Stress_Breadth_Desk_Note.pdf"
    assert pdf.exists()
    assert pdf.stat().st_size > 1000

    reader = PdfReader(str(pdf))
    assert len(reader.pages) == 1
