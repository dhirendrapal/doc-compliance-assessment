import os
import pytest
from fastapi.testclient import TestClient
from app import app, UPLOAD_DIR, MODIFIED_DIR

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clean_tmp_dirs():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(MODIFIED_DIR, exist_ok=True)

    # clean before each test
    for folder in [UPLOAD_DIR, MODIFIED_DIR]:
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))

    yield
