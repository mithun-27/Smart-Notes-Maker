# backend/pdf_utils.py

from io import BytesIO
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_stream) -> str:
    """
    file_stream: a file-like object (e.g. from Flask's request.files['file'])
    """
    pdf_bytes = BytesIO(file_stream.read())
    reader = PdfReader(pdf_bytes)
    text_parts = []
    for page in reader.pages:
        try:
            text_parts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(text_parts)
