# modifier.py — USES AGENT OUTPUT, NO SECOND LLM CALL

import os
from docx import Document

OUT_DIR = "/tmp/doc_modified"
os.makedirs(OUT_DIR, exist_ok=True)


def apply_agent_rewritten(paragraphs_report: list, job_id: str, original_path: str) -> str:
    """
    Create corrected document using agent results:
    paragraphs_report = report["paragraphs"]
    """
    out_path = os.path.join(OUT_DIR, f"{job_id}_agent.docx")

    doc = Document()

    for p in paragraphs_report:
        corrected = (
            p.get("llm", {}).get("rewritten")
            or p.get("text")
        )
        doc.add_paragraph(corrected.strip())

    doc.save(out_path)
    return out_path
