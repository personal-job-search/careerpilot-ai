from pathlib import Path
from docx import Document
import fitz

def extract_resume(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() == ".docx":
        doc = Document(path)
        return "\n".join(x.text for x in doc.paragraphs if x.text.strip())
    if p.suffix.lower() == ".pdf":
        pdf = fitz.open(path)
        return "\n".join(page.get_text() for page in pdf)
    raise ValueError("Supported formats: .docx and .pdf")
