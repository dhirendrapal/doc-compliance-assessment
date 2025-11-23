from fastapi.testclient import TestClient
from app import app
import io

client = TestClient(app)

def test_upload_docx(tmp_path):
    # create a simple docx in-memory
    from docx import Document
    p = tmp_path / 't.docx'
    doc = Document()
    doc.add_paragraph('This is a test')
    doc.save(str(p))

    with open(str(p), 'rb') as f:
        response = client.post('/upload', files={'file': ('t.docx', f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code == 200
    data = response.json()
    assert 'job_id' in data
    assert 'report' in data