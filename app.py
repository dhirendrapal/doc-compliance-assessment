from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Body
from fastapi.responses import JSONResponse, FileResponse
import uuid, shutil, os, zipfile
from extractor import extract_document
from agent import analyze_paragraphs
from modifier import apply_agent_rewritten
from utils import sanitize_filename

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
ALLOWED_EXTENSIONS = {".pdf", ".docx"}

UPLOAD_DIR = "/tmp/doc_uploads"
MODIFIED_DIR = "/tmp/doc_modified"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODIFIED_DIR, exist_ok=True)

app = FastAPI(title="Doc Compliance Assessment")

# In-memory job store
JOB_STORE = {}

@app.get("/")
async def index():
    return {"message": "Doc Compliance Assessment is an AI-powered document analysis and correction system!"}


@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    # 1. Validate size
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large (max 2MB)")

    # 2. Validate extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Only PDF and DOCX are allowed")

    # 3. Sanitize filename
    safe_name = sanitize_filename(file.filename)
    job_id = str(uuid.uuid4())
    final_name = f"{job_id}_{safe_name}"
    filepath = os.path.join(UPLOAD_DIR, final_name)

    # 4. Save securely
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 5. Validate PDF/DOCX internal structure
    if ext == ".pdf":
        with open(filepath, "rb") as f:
            if f.read(5) != b"%PDF-":
                raise HTTPException(400, "Invalid PDF signature")
    else:
        try:
            with zipfile.ZipFile(filepath) as z:
                if "[Content_Types].xml" not in z.namelist():
                    raise HTTPException(400, "Invalid DOCX: missing structure")
        except zipfile.BadZipFile:
            raise HTTPException(400, "Invalid DOCX: corrupted")

    # 6. Extract text
    paragraphs = extract_document(filepath)

    # 7. Analyze content
    report = analyze_paragraphs(paragraphs)

    # 8. Store job
    JOB_STORE[job_id] = {
        "original_path": filepath,
        "paragraphs": paragraphs,
        "report": report,
        "modified_paths": {}   # <- important fix
    }

    return {"job_id": job_id, "report": report}


@app.post("/modify/{job_id}")
async def modify(job_id: str):
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(404, "job not found")

    paragraphs_report = job["report"]["paragraphs"]
    original_path = job["original_path"]

    out = apply_agent_rewritten(paragraphs_report, job_id, original_path)

    job["modified_paths"]["agent"] = out

    return {
        "job_id": job_id,
        "engine": "agent",
        "modified_path": out
    }


@app.get("/download/{job_id}")
async def download(job_id: str):
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    path = job.get("modified_paths", {}).get("agent")
    if not path:
        raise HTTPException(404, "No agent-modified file available")

    return FileResponse(path, filename=os.path.basename(path))

