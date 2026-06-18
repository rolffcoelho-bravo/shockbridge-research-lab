from pathlib import Path

readme = Path("README.md")
text = readme.read_text(encoding="utf-8")

section_start = "<!-- SHOCKBRIDGE_PUBLIC_GRAPHIC_START -->"
section_end = "<!-- SHOCKBRIDGE_PUBLIC_GRAPHIC_END -->"

section = f"""
{section_start}

## Public research architecture

This repository presents the public evidence layer of ShockBridge Research Lab: a research framework for studying how stress propagates across macro-financial systems before it becomes obvious in headline data.

The figure below summarizes the public-facing logic of the project. It is intentionally conceptual and does not disclose private thresholds, weights, proprietary diagnostics, or action rules.

![ShockBridge public evidence architecture](figures/shockbridge_public_evidence_architecture.svg)

{section_end}
"""

if section_start in text and section_end in text:
    before = text.split(section_start)[0].rstrip()
    after = text.split(section_end)[1].lstrip()
    text = before + "\n\n" + section.strip() + "\n\n" + after
else:
    footer_marker = "<!-- SHOCKBRIDGE_PUBLIC_FOOTER_START -->"
    if footer_marker in text:
        before = text.split(footer_marker)[0].rstrip()
        after = footer_marker + text.split(footer_marker, 1)[1]
        text = before + "\n\n" + section.strip() + "\n\n" + after
    else:
        text = text.rstrip() + "\n\n" + section.strip() + "\n"

readme.write_text(text, encoding="utf-8")
print("README updated with public architecture graphic.")
