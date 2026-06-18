from pathlib import Path

REPO = "https://github.com/rolffcoelho-bravo/shockbridge-research-lab"
AUTHOR = "Rodolfo Pereira"
EMAIL = "rolffcoelho@hotmail.com"
WEBSITE = "www.shockbridgepulse.com"
YEAR = "2026"

FOOTER_START = "<!-- SHOCKBRIDGE_PUBLIC_FOOTER_START -->"
FOOTER_END = "<!-- SHOCKBRIDGE_PUBLIC_FOOTER_END -->"

CITATION_LINE = (
    "Pereira, R. (2026). *ShockBridge Research Lab: Public Evidence Layer for "
    "Macro-Financial Shock Transmission Research* [Computer software]. "
    f"GitHub. {REPO}"
)

FOOTER = f"""
{FOOTER_START}

---

## Citation and attribution

If you use, reference, quote, adapt, or build from this public research evidence layer, please cite:

{CITATION_LINE}

Author: {AUTHOR}  
Website: {WEBSITE}  
Email: {EMAIL}  

© {YEAR} {AUTHOR}. Free to read and use with attribution. Please cite the author and repository when referencing this work.

{FOOTER_END}
"""

def apply_footer(path: Path):
    text = path.read_text(encoding="utf-8")

    # Remove previous managed footer if present.
    if FOOTER_START in text and FOOTER_END in text:
        text = text.split(FOOTER_START)[0].rstrip()

    # Replace old wording if it exists outside the managed footer.
    text = text.replace(
        "Pereira, R. (2026). *ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research*. Python. GitHub.",
        "Pereira, R. (2026). *ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research* [Computer software]. GitHub."
    )
    text = text.replace(
        "Pereira, R. (2026). ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research. Python. GitHub.",
        "Pereira, R. (2026). ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research [Computer software]. GitHub."
    )

    path.write_text(text.rstrip() + "\n\n" + FOOTER.strip() + "\n", encoding="utf-8")
    print(f"Updated footer: {path}")

targets = [
    Path("README.md"),
    Path("DATA_POLICY.md"),
    Path("PORTFOLIO_MAP.md"),
    Path("PUBLIC_EVIDENCE_BOUNDARY.md"),
    Path("reports/example_research_report.md"),
]

targets += sorted(Path("docs").glob("*.md"))

for path in targets:
    if path.exists():
        apply_footer(path)

citation_cff = f"""cff-version: 1.2.0
message: "If you use, reference, quote, adapt, or build from this project, please cite it as below."
title: "ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research"
version: "v4.3-public-evidence-layer"
date-released: "2026-06-18"
url: "{REPO}"
authors:
  - family-names: "Pereira"
    given-names: "Rodolfo"
preferred-citation:
  type: software
  authors:
    - family-names: "Pereira"
      given-names: "Rodolfo"
  title: "ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research"
  year: {YEAR}
  url: "{REPO}"
"""

Path("CITATION.cff").write_text(citation_cff, encoding="utf-8")
print("Updated: CITATION.cff")

notice = f"""# Notice

ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research

If you use, reference, quote, adapt, or build from this public research evidence layer, please cite:

{CITATION_LINE}

Author: {AUTHOR}  
Website: {WEBSITE}  
Email: {EMAIL}  

© {YEAR} {AUTHOR}. Free to read and use with attribution. Please cite the author and repository when referencing this work.
"""

Path("NOTICE.md").write_text(notice, encoding="utf-8")
print("Updated: NOTICE.md")

license_text = f"""MIT License

Copyright (c) {YEAR} {AUTHOR}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

Citation is appreciated when referencing, quoting, adapting, or building from
the public research materials in this repository:

Pereira, R. (2026). ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research [Computer software]. GitHub.
{REPO}

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
"""

Path("LICENSE").write_text(license_text, encoding="utf-8")
print("Updated: LICENSE")

# Also update the generator itself if it exists.
script_path = Path("add_public_citation_footer.py")
if script_path.exists():
    script_path.write_text(Path(__file__).read_text(encoding="utf-8"), encoding="utf-8")
