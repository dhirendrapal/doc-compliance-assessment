from modifier import apply_agent_rewritten
import os
from docx import Document

def test_modifier_creates_docx(tmp_path):
    paragraphs_report = [
        {"text": "Test.", "llm": {"rewritten": "Corrected text."}}
    ]

    output = apply_agent_rewritten(paragraphs_report, "job123", None)

    assert os.path.exists(output)

    doc = Document(output)
    assert doc.paragraphs[0].text == "Corrected text."
