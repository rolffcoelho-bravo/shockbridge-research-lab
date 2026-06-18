from generate_public_research_brief import build_public_research_brief
from generate_regime_question_one_page import build_regime_question_one_page

if __name__ == "__main__":
    md_output = build_public_research_brief()
    one_page_output = build_regime_question_one_page()

    print("ShockBridge public demo complete.")
    print(f"Generated Markdown: {md_output}")
    print(f"Generated One-Page Research Desk Artifact: {one_page_output}")
