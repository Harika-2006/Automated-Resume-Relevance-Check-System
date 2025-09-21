import pdfplumber
import docx2txt
from pathlib import Path

def extract_text_from_file(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"{path} not found")
    text = ""
    if p.suffix.lower() == ".pdf":
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif p.suffix.lower() in [".docx", ".doc"]:
        text = docx2txt.process(path) or ""
    else:
        text = p.read_text(encoding="utf-8")
    return " ".join(text.split())
