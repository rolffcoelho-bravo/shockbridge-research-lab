from generate_public_research_brief import build_public_research_brief
from generate_public_question_graphic import build_public_question_graphic

try:
    from generate_public_pdf import build_public_pdf
except Exception:
    build_public_pdf = None


if __name__ == "__main__":
    md_output = build_public_research_brief()
    graphic_output = build_public_question_graphic()

    print("ShockBridge public demo complete.")
    print(f"Generated Markdown: {md_output}")
    print(f"Generated Graphic: {graphic_output}")

    if build_public_pdf is not None:
        pdf_output = build_public_pdf()
        print(f"Generated PDF: {pdf_output}")
