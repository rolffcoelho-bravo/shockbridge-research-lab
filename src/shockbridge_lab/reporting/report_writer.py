"""Report writing utilities."""

from pathlib import Path


def write_text_report(output_path: str | Path, title: str, body: str) -> Path:
    """Write a simple markdown report."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    content = f"# {title}\n\n{body}\n"
    path.write_text(content, encoding="utf-8")

    return path
