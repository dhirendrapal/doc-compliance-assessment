import os
from fastapi.testclient import TestClient
from app import UPLOAD_DIR
from app import app

client = TestClient(app)

def test_upload_docx():
    file_path = "tests/sample.docx"

    # create a small docx file for testing
    from docx import Document
    doc = Document()
    doc.add_paragraph("This is a sample.")
    doc.save(file_path)

    with open(file_path, "rb") as f:
        resp = client.post(
            "/upload",
            files={"file": ("sample.docx", f, "application/vnd.openxmlformats")}
        )

    assert resp.status_code == 200
    data = resp.json()
    assert "job_id" in data
    assert "report" in data
