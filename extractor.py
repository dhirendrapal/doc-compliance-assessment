from docx import Document
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

def extract_docx(path):
    doc = Document(path)
    paragraphs = []
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if text:
            paragraphs.append({"text": text, "paragraph_index": i, "source": "docx"})
    return paragraphs


def extract_pdf(path):
    doc = fitz.open(path)
    paragraphs = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text('text')
        if text.strip():
            for para in text.split('\n\n'):
                para = para.strip()
                if para:
                    paragraphs.append({"text": para, "page": page_num+1, "source": "pdf_text"})
        else:
            # possible scanned PDF — fallback OCR on page image
            pix = page.get_pixmap(dpi=150)
            img = Image.open(io.BytesIO(pix.tobytes()))
            ocr_text = pytesseract.image_to_string(img)
            for para in ocr_text.split('\n\n'):
                para = para.strip()
                if para:
                    paragraphs.append({"text": para, "page": page_num+1, "source": "pdf_ocr"})
    return paragraphs


def extract_document(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        return extract_pdf(path)
    elif ext == '.docx':
        return extract_docx(path)
    else:
        raise ValueError('unsupported')