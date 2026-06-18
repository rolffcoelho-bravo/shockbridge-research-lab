from pathlib import Path
import re

readme = Path("README.md")
text = readme.read_text(encoding="utf-8")

start = "<!-- SHOCKBRIDGE_QUESTION_GRAPHIC_START -->"
end = "<!-- SHOCKBRIDGE_QUESTION_GRAPHIC_END -->"

block = f"""
{start}

## The core research question

**When does a market shock become a regime problem?**

The public demo generates the figure below. It is intentionally public-safe: it explains the research logic without exposing private thresholds, weights, proprietary diagnostics, or action rules.

![ShockBridge regime question map](figures/shockbridge_regime_question_map.svg)

{end}
"""

text = re.sub(
    rf"\n?{re.escape(start)}.*?{re.escape(end)}\n?",
    "\n",
    text,
    flags=re.DOTALL,
)

lines = text.splitlines()
insert_at = 1

for i, line in enumerate(lines):
    if line.startswith("# "):
        insert_at = i + 1
        break

lines.insert(insert_at, "")
lines.insert(insert_at + 1, block.strip())

readme.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
print("README updated with front-page research question graphic.")
